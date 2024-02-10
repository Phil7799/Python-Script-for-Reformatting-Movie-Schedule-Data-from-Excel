import pandas as pd

# Read the original Excel file into a pandas DataFrame
original_data = pd.read_excel('PANARI.xlsx')

# Create a new DataFrame for the desired format
desired_format = pd.DataFrame(columns=['Movie Name', 'DateTimes'])

# Define a function to convert 12-hour time to 24-hour time
def convert_to_24hr(time_str):
    if time_str:
        dt = pd.to_datetime(time_str.strip(), format='%I:%M%p', errors='coerce')
        return dt.strftime('%H:%M') if pd.notna(dt) else ''
    else:
        return ''

# Iterate through rows of the original data and reformat it
for index, row in original_data.iterrows():
    movie_name = row['MOVIE']
    date = row['DATE'].strftime('%Y-%m-%d')
    
    # Handle potential leading/trailing whitespaces in the TIME column
    times = [time.strip() for time in row['TIME'].split(',')]

    # Convert times to 24-hour format and create a comma-separated date-time string
    date_times = []
    for i in range(9):
        if i < len(times):
            time_24hr = convert_to_24hr(times[i])
            if time_24hr:
                date_time_pair = f'{date} {time_24hr},'
                date_times.append(date_time_pair)
        else:
            date_times.append('')  # or any default value for missing times

    data_to_append = {'Movie Name': movie_name, 'DateTimes': ''.join(date_times)}
    desired_format = pd.concat([desired_format, pd.DataFrame(data_to_append, index=[0])], ignore_index=True)

# Save the reformatted data to a new Excel file
desired_format.to_excel('panari_.xlsx', index=False)