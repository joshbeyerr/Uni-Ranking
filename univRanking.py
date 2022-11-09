def loadCSVData(filename):
    # This function is intended to load the content of filename and return the content in a list format
    lister = []
    lineCount = 0

    try:

        fileContent = open(filename, "r", encoding='utf8')
        for line in fileContent:

            # If first line in csv
            if lineCount != 0:
                # Cleaning up csv text and organizing it by seperaring by commas
                line = line.strip()
                line = line.split(',')

                # Adding all important information to our list
                if filename == 'TopUni.csv':
                    lister.append([line[0].upper(), line[1].upper(), line[2].upper(), line[3].upper(), line[8].upper()])
                elif filename == 'capitals.csv':
                    lister.append([line[0].upper(), line[1].upper(), line[5].upper()])

            lineCount += 1

        fileContent.close()

    except FileNotFoundError:
        print('Cannot find file {}'.format(filename))
    return lister


def combining(topUni, capitals):
    fullList = []
    for x in topUni:
        for i in capitals:
            # if country in capitals list is within our universities list, than we combine the two thus adding
            # the capital and continent to our university list

            if i[0] in x:
                thisList = [i[1], i[2]]
                fullList.append(x + thisList)

    return fullList


def getCountries(combinedList):
    # creating a list of all countries with top universities in them, making sure countries name only appears once
    countries = []

    for x in combinedList:
        if x[2] not in countries:
            countries.append(x[2])

    return countries


def getContinents(capitals):
    continents = {}
    for x in capitals:
        continent = x[2].upper()
        if continent not in continents:
            continents[continent] = [x[0].upper()]
        else:
            continents[continent].append(x[0].upper())
    return continents


def organizeByCountry(combinedList):
    uniByCountry = {}
    for x in combinedList:
        country = x[2].upper()
        if country in uniByCountry:
            uniByCountry[country].append([x[0], x[1], x[3], x[4]])

        else:
            # If country not already in our dictionary, create new dictionary key and add the list of university
            # organizing in the order of 'international rank', 'university name', 'national rank', 'score',
            uniByCountry[country] = [[x[0], x[1], x[3], x[4]]]

    return uniByCountry


def highNational(aa):
    highestNational = 100
    for x in aa:
        # if national rank number is less than the highest national variable (aka higher ranked), it is our new best
        # national university
        if int(x[2]) < highestNational:
            highestNational = int(x[2])
            uniName = x[1]

    # returning the national rank and the name of the university
    return highestNational, uniName


def formattingOutput(f, formatInput):
    # function that clearly writes out information in a list into output.txt

    count = 0
    for x in formatInput:
        # using a counter to not print a comma for the last country in our list
        count += 1
        if count != len(formatInput):
            f.write('{}, '.format(x))
        else:
            f.write('{}'.format(x))
    f.write('\n\n')


def getInformation(selectedCountry, file1, file2):
    TOPUNI = loadCSVData(file1)
    CAPITALS = loadCSVData(file2)

    # this function combines the two lists using nested for loops
    COMBINEDLIST = combining(TOPUNI, CAPITALS)

    # 1
    numberOne = 'Total number of universities => {} \n\n'.format(len(COMBINEDLIST))
    with open('output.txt', 'w', encoding='utf8') as f:
        f.write(numberOne)

        # 2
        f.write('Available countries => ')
        COUNTRIES = getCountries(COMBINEDLIST)
        formattingOutput(f, COUNTRIES)

        # 3
        # function that created a dictionary which organizes all countries within their continent
        CONTINENTS = getContinents(CAPITALS)

        f.write('Available continents => ')
        formattingOutput(f, CONTINENTS)

        # 4 and 5
        orgCountry = organizeByCountry(COMBINEDLIST)
        # taking in the user selected country, setting to upper case to keep things consistent
        enterCountry = selectedCountry.upper()

        # If user inputted country is in our list of university countries
        if enterCountry in orgCountry:
            f.write('Universities within {}: \n'.format(enterCountry))
            aa = orgCountry[enterCountry]
            # Number of universities in the top 100 within selected country
            numberInCountry = len(aa)
            totalScore = 0

            # Going through each university to get specific information
            for x in aa:
                f.write('At international rank => {} the university name is => {} \n'.format(x[0], x[1]))

                # adding score of each university in selected country to the total score counter
                totalScore += float(x[3])

            # Determining the highest ranking national university
            highestNational = highNational(aa)
            f.write('\n')
            f.write('At national rank => {} the university name is => {} \n\n'.format(highestNational[0],
                                                                                      highestNational[1]))

            # 6
            averageScore = round((totalScore / numberInCountry), 2)
            f.write('The average score => {}% \n\n'.format(averageScore))

            # 7

            # searching for continent of our selected country in continent list that was created earlier
            for x in CONTINENTS:

                if enterCountry in CONTINENTS[x]:
                    continent = x

            # Now going through our full info list and checking for highest score in the continent
            highestScore = 0

            for x in COMBINEDLIST:
                if x[6].upper() == continent:
                    # if the score is higher than previous scores (finding the highest score)
                    score = float(x[4])
                    if score > highestScore:
                        highestScore = score

            f.write('Highest score in the continent {}\n'.format(highestScore))
            relativeScore = round(((averageScore / highestScore) * 100), 2)
            f.write('The relative score to the top university in {} is => ({} / {}) x 100% = {}% \n\n'.format(continent,averageScore,highestScore,relativeScore))

            # 8 searching through our capitals list, finding the list with our selected country, and getting the
            # capital based on index
            for x in CAPITALS:
                if enterCountry == x[0].upper():
                    capital = x[1]

            f.write('The capital is => {} \n\n'.format(capital))

            # 9
            f.write('The universities that contain the capital name => \n')
            count = 0

            # searching through all universities within our country
            for x in orgCountry[enterCountry]:
                # if the capital city is in the university name than...
                if capital in x[1]:
                    count += 1
                    f.write('#{} {} \n'.format(count, x[1]))


getInformation('canada', "TopUni.csv", "capitals.csv")