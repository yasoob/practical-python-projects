import os
from flask import Flask, request
import requests
from dateutil import parser, tz
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
to_zone = tz.gettz('America/New_York')

countries = ['KOR', 'PAN', 'MEX', 'ENG', 'COL', 'JPN', 'POL', 'SEN', 
                'RUS', 'EGY', 'POR', 'MAR', 'URU', 'KSA', 'IRN', 'ESP', 
                'DEN', 'AUS', 'FRA', 'PER', 'ARG', 'CRO', 'BRA', 'CRC', 
                'NGA', 'ISL', 'SRB', 'SUI', 'BEL', 'TUN', 'GER', 'SWE']

urls = {'group': 'http://worldcup.sfg.io/teams/group_results',
        'country': 'http://worldcup.sfg.io/matches/country?fifa_code=',
        'today': 'http://worldcup.sfg.io/matches/today',
        'tomorrow': 'http://worldcup.sfg.io/matches/tomorrow'
}

@app.route('/', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()

    if body == 'today':
        html = requests.get(urls['today']).json()
        output = "\n"
        for match in html:
            output += (
                match['home_team_country'] + " vs " +
                match['away_team_country'] + " at " +
                parser.parse(match['datetime']).astimezone(to_zone)
                    .strftime('%I:%M %p') + "\n"
            )
        else:
            output += "No matches happening today"

    elif body == 'tomorrow':
        html = requests.get(urls['tomorrow']).json()
        output = "\n"
        for match in html:
            output += (
                match['home_team_country'] + " vs " +
                match['away_team_country'] + " at " +
                parser.parse(match['datetime']).astimezone(to_zone)
                    .strftime('%I:%M %p') + "\n"
            )
        else:
            output += "No matches happening tomorrow"

    elif body.upper() in countries:
        html = requests.get(urls['country']+body).json()
        output = "\n--- Past Matches ---\n"
        for match in html:
            if match['status'] == 'completed':
                output += (
                    match['home_team']['country'] + " " +
                    str(match['home_team']['goals']) + " vs " +
                    match['away_team']['country'] + " " +
                    str(match['away_team']['goals']) + "\n"
                )

        output += "\n\n--- Future Matches ---\n"
        for match in html:
            if match['status'] == 'future':
                output += (
                    match['home_team']['country'] + " vs " +
                    match['away_team']['country'] + " at " +
                    parser.parse(match['datetime'])
                      .astimezone(to_zone)
                      .strftime('%I:%M %p on %d %b') + "\n"
                )
    
    elif body == 'complete':
        html = requests.get(urls['group']).json()
        output = ""
        for group in html:
            output += "\n\n--- Group " + group['letter'] + " ---\n"
            for team in group['ordered_teams']:
                output += (
                    team['country'] + " Pts: " +
                    str(team['points']) + "\n"
                )

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host='0.0.0.0', port=port)