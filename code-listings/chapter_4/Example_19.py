"""
Using This Code Example
=========================
The code examples are provided by Yasoob Khalid to help you 
reference Practical Python Projects book. Code samples follow
PEP-0008, with exceptions made for the purposes of improving book
formatting. Example code is provided "as is".
Permissions
============
In general, you may use the code we've provided with this book in your
programs . You do not need to contact us for permission unless you're
reproducing a significant portion of the code and using it in educational
distributions. Examples:
* Writing an education program or book that uses several chunks of code from
    this course requires permission. 
* Selling or distributing a digital package from material taken from this
    book does require permission.
* Answering a question by citing this book and quoting example code does not
    require permission.
Attributions usually include the title, author, publisher and an ISBN. For
example, "Practical Python Projects, by Yasoob Khalid. Copyright 2020 Yasoob."
If you feel your use of code examples falls outside fair use of the permission
given here, please contact me at hi@yasoob.me.
"""

# ...
urls = {'group': 'https://worldcup.sfg.io/teams/group_results',
        'country': 'https://worldcup.sfg.io/matches/country?fifa_code=',
        'today': 'https://worldcup.sfg.io/matches/today',
        'tomorrow': 'https://worldcup.sfg.io/matches/tomorrow'
}
#...
@app.route('/', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    if body == 'today':
        data = requests.get(urls['today']).json()
        output = "\n"
        for match in data:
            output += match['home_team_country'] + ' vs ' + \
            match['away_team_country'] + " at " + \
            parser.parse(match['datetime']).astimezone(to_zone)
                .strftime('%I:%M %p') + "\n"
        else:
            output += "No matches happening today"
    elif body == 'tomorrow':
        data = requests.get(urls['tomorrow']).json()
        output = "\n"
        for match in data:
            output += match['home_team_country'] + ' vs ' + \
            match['away_team_country'] + " at " + \
            parser.parse(match['datetime']).astimezone(to_zone)
                .strftime('%I:%M %p') + "\n"
        else:
            output += "No matches happening tomorrow"
    elif body.upper() in countries:
        data = requests.get(urls['country']+body).json()
        output = "\n--- Past Matches ---\n"
        for match in data:
            if match['status'] == 'completed':
                output += match['home_team']['country'] + " " + \
                          str(match['home_team']['goals']) + " vs " + \
                          match['away_team']['country']+ " " + \
                          str(match['away_team']['goals']) + "\n"
        output += "\n\n--- Future Matches ---\n"
        for match in data:
            if match['status'] == 'future':
                output += match['home_team']['country'] + " vs " + \
                          match['away_team']['country'] + " at " + \
                          parser.parse(match['datetime']).astimezone(to_zone)
                            .strftime('%I:%M %p on %d %b') +"\n"
    
    elif body == 'complete':
        data = requests.get(urls['group']).json()
        output = ""
        for group in data:
            output += "\n\n--- Group " + group['letter'] + " ---\n"
            for team in group['ordered_teams']:
                output += team['country'] + " Pts: " + \
                            str(team['points']) + "\n"
    elif body == 'list':
        output = '\n'.join(countries)
    else:
        output = ('Sorry we could not understand your response. '
            'You can respond with "today" to get today\'s details, '
            '"tomorrow" to get tomorrow\'s details, "complete" to '
            'get the group stage standing of teams or '
            'you can reply with a country FIFA code (like BRA, ARG) '
            'and we will send you the standing of that particular country. '
            'For a list of FIFA codes send "list".\n\nHave a great day!')
    resp.message(output)
    return str(resp)
