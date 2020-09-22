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

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    posted_data = request.get_json() or {}
    today = datetime.today().strftime("%B %-d, %Y")
    default_data = {
        'duedate': 'August 1, 2019',
        'from_addr': {
            'addr1': '12345 Sunny Road',
            'addr2': 'Sunnyville, CA 12345',
            'company_name': 'Python Tip'
        },
        'invoice_number': 123,
        'items': [{
                'charge': 300.0,
                'title': 'website design'
            },
            {
                'charge': 75.0,
                'title': 'Hosting (3 months)'
            },
            {
                'charge': 10.0,
                'title': 'Domain name (1 year)'
            }
        ],
        'to_addr': {
            'company_name': 'Acme Corp',
            'person_email': 'john@example.com',
            'person_name': 'John Dilly'
        }
    }
    duedate = posted_data.get('duedate', default_data['duedate'])
    from_addr = posted_data.get('from_addr', default_data['from_addr'])
    to_addr = posted_data.get('to_addr', default_data['to_addr'])
    invoice_number = posted_data.get('invoice_number', 
                                      default_data['invoice_number'])
    items = posted_data.get('items', default_data['items'])
    total = sum([i['charge'] for i in items])
    rendered = render_template('invoice.html', 
                            date = today, 
                            from_addr = from_addr,
                            to_addr = to_addr,
                            items = items,
                            total = total, 
                            invoice_number = invoice_number,
                            duedate = duedate)
    html = HTML(string=rendered)
    rendered_pdf = html.write_pdf()
    return send_file(
            io.BytesIO(rendered_pdf),
            attachment_filename='invoice.pdf'
        )
