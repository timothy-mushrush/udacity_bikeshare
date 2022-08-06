import pandas as pd
import time


# Month information
# "Original"
month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
              'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
month_key_list = list(month_dict.keys())
month_value_list = list(month_dict.values())
# Lower-case
month_dict_lower = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
                    'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
month_key_list_lower = list(month_dict_lower.keys())

# Day of the week information
# "Original"
day_dict = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
day_key_list = list(day_dict.keys())
day_value_list = list(day_dict.values())
# Lower-case
day_dict_lower = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                  'sunday': 6}
day_key_list_lower = list(day_dict_lower.keys())


def input_filter():
    """
    Asks user to specify a city, month, and day of the week to analyze.

    Args:

    Returns:
        (str) city - name of the city to analyze
        (str) month_input - name of the month to filter by, or "all" to apply no month filter
        (str) day_input - name of the day of week to filter by, or "all" to apply no day filter

    """
    # City
    while True:
        city = input('\nInput city to analyze. Enter either Chicago, New York City, or Washington.\n')
        if (city.lower() == 'chicago') or (city.lower() == 'new york city') or (city.lower() == 'washington'):
            break
        else:
            print('Incorrect input for city. Input one of the following:')
            print('Chicago\nNew York City\nWashington\n')
    # Month
    while True:
        month_input = input('Input month to analyze (January, February, etc) or enter \"all\" for all months.\n')
        if (month_input.lower() in month_key_list_lower) or (month_input.lower() == 'all'):
            break
        else:
            print('Incorrect input for month. Input \"all\" or a month. Month should be spelled out as shown.')
            print('January, February, March, April, May, June, July, August, September, October, November, December')
    # Day of the week
    while True:
        day_input = input('Input day of week to analyze (Sunday, Monday, etc) or enter \"all\" for all days.\n')
        if (day_input.lower() in day_key_list_lower) or (day_input.lower() == 'all'):
            break
        else:
            print('Incorrect input for day of the week. Input \"all\" or a day. Day should be spelled out as shown:')
            print('Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n')
    print('-'*40)
    return city, month_input, day_input


def load_data(city, month_input, day_input):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month_input - name of the month to filter by, or "all" to apply no month filter
        (str) day_input - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('Loading data based on user inputs...\n\n')
    function_start_time = time.time()
    if city.lower() == 'chicago':
        df = pd.read_csv('chicago.csv')
    elif city.lower() == 'new york city':
        df = pd.read_csv('new_york_city.csv')
    elif city.lower() == 'washington':
        df = pd.read_csv('washington.csv')
    else:
        print('There was an error loading the city data. Review inputs.')
    # Convert df "Start Time" column to the datetime column type
    df['start_time'] = pd.to_datetime(df['Start Time'])
    # Create month column in df
    df['start_month'] = df.start_time.dt.month
    if month_input.lower() != 'all':
        df = df[df['start_month'] == month_dict_lower[month_input.lower()]]
    else:
        pass
    # Create day of the week column in df
    df['start_day_of_week'] = df.start_time.dt.dayofweek
    if day_input.lower() != 'all':
        df = df[df['start_day_of_week'] == day_dict_lower[day_input.lower()]]
    else:
        pass
    # Create hour column in df
    df['start_hour'] = df.start_time.dt.hour
    print(f'It took {(time.time() - function_start_time)} seconds to load the data')
    print('-' * 40)
    return df


def time_stats(df, city, month_input, day_input):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city that is being analyzed
        (str) month_input - name of the month to filter by, or "all" to apply no month filter
        (str) day_input - name of the day of week to filter by, or "all" to apply no day filter

    Returns:

    """
    print('Calculating the most frequent times of travel...\n\n')
    function_start_time = time.time()
    # Capitalize input
    city_cap = city.capitalize()
    month_cap = month_input.capitalize()
    day_cap = day_input.capitalize()
    # Most common times
    most_common_month = month_key_list[int(df['start_month'].mode()) - 1]
    most_common_day = day_key_list[int(df['start_day_of_week'].mode())]
    most_common_hour = int(df['start_hour'].mode())
    if most_common_hour == 0:
        most_common_hour = str(12) + 'AM'
    elif most_common_hour <= 11:
        most_common_hour = str(most_common_hour)+'AM'
    else:
        most_common_hour = str(most_common_hour-12) + 'PM'
    # Output to terminal
    if month_input.lower() == 'all':
        if day_input.lower() == 'all':
            print(f'The most common month of travel in {city_cap} is: {most_common_month}.')
            print(f'The most common day of the week to travel on in {city_cap} is {most_common_day}.')
            print(f'Most common hour of travel in {city_cap} is {most_common_hour}.')
        else:
            print(f'For {day_cap}s the most common month of travel in {city_cap} is {most_common_month}.')
            print(f'On {day_cap}s the most common hour of travel in {city_cap} is {most_common_hour}.')
    else:
        if day_input.lower() == 'all':
            print(f'In {city_cap} the most common day of the week to travel on in {month_cap} is {most_common_day}.')
            print(f'In {city_cap} the most common hour to travel on in {month_cap} is {most_common_hour}.')
        else:
            print(f'In {city_cap} the most common travel time on {day_cap}s in {month_cap} is {most_common_hour}.')
    print()
    print(f'It took {(time.time() - function_start_time)} seconds to calculate these time statistics')
    print('-'*40)
    return None


def station_stats(df, city, month_input, day_input):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city that is being analyzed
        (str) month_input - name of the month to filter by, or "all" to apply no month filter
        (str) day_input - name of the day of week to filter by, or "all" to apply no day filter

    Returns:

    """
    print('Calculating the most popular stations and trip...\n\n')
    function_start_time = time.time()
    # Capitalize input
    city_cap = city.capitalize()
    month_cap = month_input.capitalize()
    day_cap = day_input.capitalize()
    # Most common stations
    most_common_start = df['Start Station'].mode().to_string(index=False)
    most_common_end = df['End Station'].mode().to_string(index=False)
    # Most common trip
    df['trip_stations'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trip = df['trip_stations'].mode().to_string(index=False)
    # Output to terminal
    if month_input.lower() == 'all':
        if day_input.lower() == 'all':
            print(f'The most common start station in {city_cap} is {most_common_start}.')
            print(f'The most common end station in {city_cap} is {most_common_end}.')
            print(f'The most common trip taken in {city_cap} is {most_common_trip}.')
        else:
            print(f'On {day_cap}s the most common start station in {city_cap} is {most_common_start}.')
            print(f'On {day_cap}s the most common end station in {city_cap} is {most_common_end}.')
            print(f'On {day_cap}s the most common trip taken in {city_cap} is {most_common_trip}.')
    else:
        if day_input == 'all':
            print(f'In {month_cap} the most common start station in {city_cap} is {most_common_start}.')
            print(f'In {month_cap} the most common end station in {city_cap} is {most_common_end}.')
            print(f'In {month_cap} the most common trip taken in {city_cap} is {most_common_trip}.')
        else:
            print(f'For {day_cap}s in {month_cap}, {city_cap}\'s most common start station is {most_common_start}.')
            print(f'For {day_cap}s in {month_cap}, {city_cap}\'s most common end station is {most_common_end}.')
            print(f'For {day_cap}s in {month_cap}, {city_cap}\'s most common trip taken is {most_common_trip}.')
    print()
    print(f'It took {(time.time() - function_start_time)} seconds to calculate the station statistics')
    print('-'*40)


def trip_duration_stats(df, city, month_input, day_input):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city that is being analyzed
        (str) month_input - name of the month to filter by, or "all" to apply no month filter
        (str) day_input - name of the day of week to filter by, or "all" to apply no day filter

    Returns:

    """
    print('Calculating trip duration...\n\n')
    function_start_time = time.time()
    # Capitalize input
    city_cap = city.capitalize()
    month_cap = month_input.capitalize()
    day_cap = day_input.capitalize()
    # Total travel time
    tot_travel = df['Trip Duration'].sum()
    # Average travel time
    avg_travel = df['Trip Duration'].mean()
    # Output to terminal
    if month_input.lower() == 'all':
        if day_input.lower() == 'all':
            print(f'The total travel time in {city_cap} is {tot_travel} seconds.')
            print(f'The average travel time in {city_cap} is {avg_travel} seconds.')
        else:
            print(f'On {day_cap}s in {city_cap} the total travel time is {tot_travel} seconds.')
            print(f'On {day_cap}s in {city_cap} the average travel time is {avg_travel} seconds.')
    else:
        if day_input == 'all':
            print(f'The total travel time in {city_cap} during {month_cap} is {tot_travel} seconds.')
            print(f'The average travel time in {city_cap} during {month_cap} is {avg_travel} seconds.')
        else:
            print(f'In {city_cap} the total travel time on {day_cap}s in {month_cap} is {tot_travel} seconds.')
            print(f'In {city_cap} the average travel time on {day_cap}s in {month_cap} is {avg_travel} seconds.')

    print(f'\nIt took {(time.time() - function_start_time)} seconds to calculate the duration statistics')
    print('-'*40)


def user_stats(df, city, month_input, day_input):
    """
    Displays statistics on bikeshare users.

    Args:
        (pandas.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city that is being analyzed
        (str) month_input - name of the month to filter by, or "all" to apply no month filter
        (str) day_input - name of the day of week to filter by, or "all" to apply no day filter

    Returns:

    """
    function_start_time = time.time()
    print('\nCalculating user stats...\n')
    # Capitalize input
    city_cap = city.capitalize()
    month_cap = month_input.capitalize()
    day_cap = day_input.capitalize()
    # Count of each user type
    user_type_list = df['User Type'].unique()
    user_type_count_list = []
    for user_type in user_type_list:
        user_type_count_list += [len(df[df['User Type'] == user_type])]
    user_type_dict = dict(zip(user_type_list, user_type_count_list))
    # Count of each gender
    if city.lower() == 'washington':
        pass
    else:
        user_gender_key = df['Gender'].unique()
        user_gender_count = []
        for user_gender in user_gender_key:
            user_gender_count += [len(df[df['Gender'] == user_gender])]
        user_gender_dict = dict(zip(user_gender_key, user_gender_count))
    # Earliest, most recent, and most common year of birth
    if city.lower() == 'washington':
        pass
    else:
        earliest_by = int(df['Birth Year'].min())
        latest_by = int(df['Birth Year'].max())
        most_common_by = int(df['Birth Year'].mode())
    # Display to terminal
    if city.lower() == 'washington':
        if month_input.lower() == 'all':
            if day_input.lower() == 'all':
                print(f'In Washington the number of each user type can be seen below:')
                print(user_type_dict)
            else:
                print(f'In Washington the number of each user type on {day_cap}s are below:')
                print(user_type_dict)
        else:
            if day_input.lower() == 'all':
                print(f'In Washington the number of each user type for {month_cap} are below:')
                print(user_type_dict)
            else:
                print(f'In Washington the number of each user type for {day_cap}s in {month_cap} are below:')
                print(user_type_dict)
    else:
        if month_input.lower() == 'all':
            if day_input.lower() == 'all':
                print(f'In {city_cap} the number of each user type can be seen below:')
                print(user_type_dict)
                print(f'In {city_cap} the number of each gender can be seen below:')
                print(user_gender_dict)
                print(f'In {city_cap} the earliest (oldest) birth year is {earliest_by}.')
                print(f'In {city_cap} the most recent (youngest) birth year is {latest_by}.')
                print(f'In {city_cap} the most common birth year is {most_common_by}.')
            else:
                print(f'In {city_cap} the number of each user type on {day_cap}s can be seen below:')
                print(user_type_dict)
                print(f'In {city_cap} the number of each gender on {day_cap}s can be seen below:')
                print(user_gender_dict)
                print(f'In {city_cap} the earliest (oldest) birth year on {day_cap}s is {earliest_by}.')
                print(f'In {city_cap} the most recent (youngest) birth year on {day_cap}s is {latest_by}.')
                print(f'In {city_cap} the most common birth year on {day_cap}s is {most_common_by}.')
        else:
            if day_input.lower() == 'all':
                print(f'In {city_cap} the number of each user type in {month_cap} can be seen below:')
                print(user_type_dict)
                print(f'In {city_cap} the number of each gender in {month_cap} can be seen below:')
                print(user_gender_dict)
                print(f'In {city_cap} the earliest (oldest) birth year in {month_cap} is {earliest_by}.')
                print(f'In {city_cap} the most recent (youngest) birth year in {month_cap} is {latest_by}.')
                print(f'In {city_cap} the most common birth year in {month_cap} is {most_common_by}.')
            else:
                print(f'In {city_cap} the number of each user type on {day_cap}s in {month_cap} can be seen below:')
                print(user_type_dict)
                print(f'In {city_cap} the number of each gender on {day_cap}s in {month_cap} can be seen below:')
                print(user_gender_dict)
                print(f'In {city_cap} the earliest (oldest) birth year on {day_cap}s in {month_cap} is {earliest_by}.')
                print(f'In {city_cap} the most recent birth year on {day_cap}s in {month_cap} is {latest_by}.')
                print(f'In {city_cap} the most common birth year on {day_cap}s in {month_cap} is {most_common_by}.')
    print(f'\nIt took {(time.time() - function_start_time)} seconds to calculate the user statistics')
    print('-' * 40)


def main():
    print('\nHello! Let\'s explore some US bikeshare data!')
    while True:
        city, month_input, day_input = input_filter()
        df = load_data(city, month_input, day_input)
        if len(df) == 0:
            print('There were no trips for that combination of city, month, and day of the week.')
            print('Choose a different combination of inputs.')
            break
        time_stats(df, city, month_input, day_input)
        station_stats(df, city, month_input, day_input)
        trip_duration_stats(df, city, month_input, day_input)
        user_stats(df, city, month_input, day_input)
        print(f'\nWould you like to see the raw data for your selection? (FYI: number of rows of data = {len(df)})')
        raw_data = input('Enter yes or no to see first 5 rows.\n')
        if raw_data.lower() == 'yes':
            if len(df) <= 5:
                print(df)
                print('No more raw data to load...')
            else:
                for i in range(5, len(df), 5):
                    print(df.iloc[:i])
                    test = len(df) - (i//5)*5
                    if test < 5:
                        print('No more raw data to load...')
                        print(df)
                        break
                    raw_data_continue = input('Would you like to load 5 more rows? Enter yes or no.\n')
                    if raw_data_continue.lower() != 'yes':
                        break
        else:
            pass
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
