import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional, Dict, List
import re

class DataProcessor:
    """Handles loading, cleaning, and processing of OECD maritime emissions data"""
    
    def __init__(self):
        self.required_columns = ['Country', 'Year', 'Emissions']
        self.column_mappings = {
            # Common variations for country columns
            'country': ['Country', 'COUNTRY', 'Countries', 'COUNTRIES', 'Country Name', 'Region', 'REGION', 'Location', 'LOCATION', 
                       'Reference area', 'REFERENCE_AREA', 'REF_AREA', 'Reference Area'],
            # Common variations for year columns
            'year': ['Year', 'YEAR', 'Time', 'TIME', 'Period', 'Date', 'TIME_PERIOD', 
                    'Time period', 'TIME_PERIOD', 'Time Period', 'TIME PERIOD'],
            # Common variations for emissions columns
            'emissions': ['Emissions', 'EMISSIONS', 'CO2', 'CO2_EMISSIONS', 'Value', 'VALUE', 
                         'Tonnes', 'Mt CO2', 'CO2 Emissions', 'Carbon Emissions', 'Emission',
                         'OBS_VALUE', 'Obs Value', 'Observation Value']
        }
    
    def load_and_clean_data(self, file_input) -> pd.DataFrame:
        """Load and clean Excel file from either uploaded file or file path"""
        try:
            # Handle both file paths and uploaded file objects
            if isinstance(file_input, str):
                # File path provided - try with header first, then without
                try:
                    df = pd.read_excel(file_input, sheet_name=None, header=0)
                except:
                    df = pd.read_excel(file_input, sheet_name=None, header=None)
            else:
                # Uploaded file object provided - try with header first, then without
                try:
                    df = pd.read_excel(file_input, sheet_name=None, header=0)
                except:
                    df = pd.read_excel(file_input, sheet_name=None, header=None)
            
            # If multiple sheets, try to find the main data sheet
            if isinstance(df, dict):
                sheet_names = list(df.keys())
                main_sheet = self._find_main_sheet(sheet_names)
                df = df[main_sheet]
            
            # Check if this is an OECD-structured file and process accordingly
            df = self._handle_oecd_structure(df)
            
            # Clean and standardize the data
            df = self._clean_data(df)
            
            # Validate the data
            self._validate_data(df)
            
            return df
            
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")
    
    def _find_main_sheet(self, sheet_names: List[str]) -> str:
        """Find the main data sheet from multiple sheets"""
        # Prioritize sheets that likely contain data
        priority_keywords = ['table', 'data', 'emissions', 'maritime', 'transport', 'co2', 'sheet1']
        
        for keyword in priority_keywords:
            for sheet in sheet_names:
                if keyword.lower() in sheet.lower():
                    return sheet
        
        # If no keyword match, return the first sheet
        return sheet_names[0]
    
    def _handle_oecd_structure(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle OECD-specific Excel structure with headers in specific rows"""
        try:
            # Check if this is the wide format with years as columns
            if self._is_wide_format_with_years(df):
                return self._transform_wide_to_long(df)
            
            # Check if this looks like OECD format by looking for specific patterns
            oecd_indicators = []
            for i in range(min(20, len(df))):
                row_str = df.iloc[i].dropna().astype(str).str.cat(sep=' ')
                if any(indicator in row_str.lower() for indicator in ['reference area', 'time period', 'maritime', 'emissions']):
                    oecd_indicators.append(i)
            
            if len(oecd_indicators) >= 2:
                # This looks like OECD format
                return self._parse_oecd_format(df)
            else:
                # Regular format, return as is
                return df
                
        except Exception:
            # If parsing fails, return original
            return df
    
    def _is_wide_format_with_years(self, df: pd.DataFrame) -> bool:
        """Check if DataFrame has years as column headers (wide format)"""
        if len(df.columns) < 3:
            return False
        
        # Check if column names look like years
        year_columns = 0
        for col in df.columns[1:]:  # Skip first column (usually country names)
            try:
                year = int(col)
                if 2000 <= year <= 2030:
                    year_columns += 1
            except:
                continue
        
        return year_columns >= 2
    
    def _transform_wide_to_long(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform wide format (years as columns) to long format"""
        # First column should be country names
        country_col = df.columns[0]
        
        # Get year columns (numeric columns that look like years)
        year_cols = []
        for col in df.columns[1:]:
            try:
                year = int(col)
                if 2000 <= year <= 2030:
                    year_cols.append(col)
            except:
                continue
        
        if not year_cols:
            return df
        
        # Melt the DataFrame to transform from wide to long format
        long_df = pd.melt(
            df, 
            id_vars=[country_col], 
            value_vars=year_cols,
            var_name='Year', 
            value_name='Emissions'
        )
        
        # Rename country column to standard name
        long_df = long_df.rename(columns={country_col: 'Country'})
        
        # Convert year to integer
        long_df['Year'] = long_df['Year'].astype(int)
        
        # Convert emissions to numeric, handling any string values
        long_df['Emissions'] = pd.to_numeric(long_df['Emissions'], errors='coerce')
        
        # Remove rows with missing emissions data
        long_df = long_df.dropna(subset=['Emissions'])
        
        # Clean country names
        long_df['Country'] = long_df['Country'].astype(str).str.strip()
        long_df = long_df[long_df['Country'] != 'nan']
        long_df = long_df[long_df['Country'] != '']
        
        return long_df
    
    def _parse_oecd_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse OECD-specific format with time periods as columns and countries as rows"""
        try:
            # Find the time period row (contains year-month data)
            time_row = None
            country_start_row = None
            
            for i in range(min(15, len(df))):
                row_data = df.iloc[i].dropna().astype(str)
                if len(row_data) > 5 and any('2022' in str(val) or '2021' in str(val) or '2020' in str(val) or '2019' in str(val) for val in row_data):
                    time_row = i
                    country_start_row = i + 2  # Countries usually start 2 rows after time periods
                    break
            
            if time_row is None:
                return df
            
            # Extract time periods (skip first column which is for country names)
            time_periods = df.iloc[time_row, 1:].dropna().tolist()
            
            # Extract country data starting from country_start_row
            processed_data = []
            
            for i in range(country_start_row, len(df)):
                row_data = df.iloc[i].dropna()
                if len(row_data) > 5:  # Must have country name + several data points
                    country = str(row_data.iloc[0]).strip()
                    # Clean up country name (remove special characters used for indentation)
                    country = re.sub(r'^[·\s\u2007]+', '', country)
                    
                    if country and country not in ['nan', 'NaN', '']:
                        # Get the data values for each time period
                        values = row_data.iloc[1:].tolist()
                        
                        # Create rows for each time period
                        for j, time_period in enumerate(time_periods):
                            if j < len(values) and pd.notna(values[j]):
                                try:
                                    emission_value = float(values[j])
                                    processed_data.append({
                                        'Country': country,
                                        'Time_Period': str(time_period),
                                        'Emissions': emission_value
                                    })
                                except (ValueError, TypeError):
                                    continue
            
            if processed_data:
                result_df = pd.DataFrame(processed_data)
                
                # Parse time periods to extract years
                result_df['Year'] = result_df['Time_Period'].apply(self._extract_year_from_time_period)
                
                # Rename columns to standard format
                result_df = result_df.rename(columns={'Time_Period': 'Original_Time_Period'})
                result_df = result_df[['Country', 'Year', 'Emissions', 'Original_Time_Period']]
                
                return result_df
            else:
                return df
                
        except Exception as e:
            print(f"Error parsing OECD format: {e}")
            return df
    
    def _extract_year_from_time_period(self, time_period_str):
        """Extract year from time period string like '2022-Jan' or '2022-01'"""
        try:
            time_str = str(time_period_str)
            # Extract the year part (first 4 digits)
            year_match = re.search(r'(\d{4})', time_str)
            if year_match:
                year = int(year_match.group(1))
                # Ensure reasonable year range
                if 1900 <= year <= 2030:
                    return year
            return None
        except:
            return None
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize the dataframe"""
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Only map columns if we don't already have the standard columns
        if not all(col in df.columns for col in self.required_columns):
            df = self._map_columns(df)
        
        # Clean country names
        if 'Country' in df.columns:
            df['Country'] = df['Country'].astype(str).str.strip()
            df = df[df['Country'] != 'nan']
            df = df[df['Country'] != '']
        
        # Clean year data (handle both year and year-month formats)
        if 'Year' in df.columns:
            # Check if year column is already clean (all integers)
            if not pd.api.types.is_integer_dtype(df['Year']):
                df['Year'] = self._parse_time_period(df['Year'])
                df = df.dropna(subset=['Year'])
            df['Year'] = df['Year'].astype(int)
        
        # Clean emissions data
        if 'Emissions' in df.columns:
            df['Emissions'] = pd.to_numeric(df['Emissions'], errors='coerce')
            df = df.dropna(subset=['Emissions'])
            # Remove negative emissions (likely errors)
            df = df[df['Emissions'] >= 0]
        
        # Remove any remaining rows with missing critical data
        if all(col in df.columns for col in self.required_columns):
            df = df.dropna(subset=self.required_columns)
        
        # Sort by Country and Year if both columns exist
        sort_cols = []
        if 'Country' in df.columns:
            sort_cols.append('Country')
        if 'Year' in df.columns:
            sort_cols.append('Year')
        
        if sort_cols:
            df = df.sort_values(sort_cols)
        
        return df
    
    def _map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map column names to standard format"""
        column_mapping = {}
        
        for col in df.columns:
            col_str = str(col).strip()
            
            # Map country columns
            if any(country_var.lower() == col_str.lower() for country_var in self.column_mappings['country']):
                column_mapping[col] = 'Country'
            
            # Map year columns
            elif any(year_var.lower() == col_str.lower() for year_var in self.column_mappings['year']):
                column_mapping[col] = 'Year'
            
            # Map emissions columns
            elif any(emission_var.lower() == col_str.lower() for emission_var in self.column_mappings['emissions']):
                column_mapping[col] = 'Emissions'
            
            # Check for partial matches in emissions
            elif any(emission_var.lower() in col_str.lower() for emission_var in self.column_mappings['emissions']):
                column_mapping[col] = 'Emissions'
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        return df
    
    def _parse_time_period(self, time_series):
        """Parse time period that could be year or year-month format"""
        parsed_values = []
        
        for value in time_series:
            try:
                # Convert to string and clean
                str_value = str(value).strip()
                
                # Handle different formats
                if '-' in str_value:
                    # Year-month format (e.g., "2020-01", "2020-M01")
                    year_part = str_value.split('-')[0]
                    # Remove any non-numeric characters from year part
                    year_part = re.sub(r'[^0-9]', '', year_part)
                    parsed_values.append(pd.to_numeric(year_part, errors='coerce'))
                elif 'M' in str_value.upper():
                    # Handle formats like "2020M01"
                    year_part = str_value.upper().split('M')[0]
                    year_part = re.sub(r'[^0-9]', '', year_part)
                    parsed_values.append(pd.to_numeric(year_part, errors='coerce'))
                else:
                    # Simple year format
                    numeric_value = re.sub(r'[^0-9]', '', str_value)
                    if numeric_value:
                        parsed_values.append(pd.to_numeric(numeric_value, errors='coerce'))
                    else:
                        parsed_values.append(np.nan)
                        
            except Exception:
                parsed_values.append(np.nan)
        
        return pd.Series(parsed_values, index=time_series.index)
    
    def _validate_data(self, df: pd.DataFrame) -> None:
        """Validate that the data has required columns and structure"""
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        
        if missing_columns:
            available_columns = list(df.columns)
            raise ValueError(
                f"Missing required columns: {missing_columns}. "
                f"Available columns: {available_columns}. "
                f"Please ensure your file contains data for Country/Region, Year, and CO2 Emissions."
            )
        
        if len(df) == 0:
            raise ValueError("No valid data rows found after cleaning. Please check your file format.")
        
        # Check for reasonable year range
        if 'Year' in df.columns:
            years = df['Year'].unique()
            if len(years) > 0:
                min_year, max_year = min(years), max(years)
                if min_year < 1900 or max_year > 2030:
                    st.warning(f"⚠️ Unusual year range detected: {min_year}-{max_year}. Please verify data quality.")
        
        # Check for reasonable emissions values
        if 'Emissions' in df.columns:
            max_emissions = df['Emissions'].max()
            if max_emissions > 1e9:  # Very large emissions value
                st.warning("⚠️ Very large emissions values detected. Please verify units (should be in tonnes CO2).")
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        """Generate summary statistics for the dataset"""
        if df.empty:
            return {}
        
        stats = {
            'total_records': len(df),
            'countries_count': df['Country'].nunique() if 'Country' in df.columns else 0,
            'year_range': (
                df['Year'].min(), df['Year'].max()
            ) if 'Year' in df.columns else (None, None),
            'total_emissions': df['Emissions'].sum() if 'Emissions' in df.columns else 0,
            'avg_emissions_per_country': (
                df.groupby('Country')['Emissions'].sum().mean() 
                if 'Country' in df.columns and 'Emissions' in df.columns else 0
            )
        }
        
        return stats
    
    def aggregate_by_region(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate data by regions (if regional data is available)"""
        # This is a placeholder for regional aggregation
        # In a real implementation, you might have a mapping of countries to regions
        return df.groupby(['Country', 'Year'])['Emissions'].sum().reset_index()
    
    def calculate_trends(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate emission trends for each country"""
        if 'Country' not in df.columns or 'Year' not in df.columns or 'Emissions' not in df.columns:
            return pd.DataFrame()
        
        trends = []
        for country in df['Country'].unique():
            country_data = df[df['Country'] == country].sort_values('Year')
            if len(country_data) > 1:
                # Calculate simple trend (first vs last year)
                first_year_emissions = country_data.iloc[0]['Emissions']
                last_year_emissions = country_data.iloc[-1]['Emissions']
                
                if first_year_emissions > 0:
                    trend_pct = ((last_year_emissions - first_year_emissions) / first_year_emissions) * 100
                else:
                    trend_pct = 0
                
                trends.append({
                    'Country': country,
                    'First_Year': country_data.iloc[0]['Year'],
                    'Last_Year': country_data.iloc[-1]['Year'],
                    'First_Year_Emissions': first_year_emissions,
                    'Last_Year_Emissions': last_year_emissions,
                    'Trend_Percentage': trend_pct,
                    'Trend_Direction': 'Increasing' if trend_pct > 0 else 'Decreasing' if trend_pct < 0 else 'Stable'
                })
        
        return pd.DataFrame(trends)