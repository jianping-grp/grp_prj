import urllib2
from bs4 import BeautifulSoup as bs

# table id
TABLE_ID = {
    'PATHWAY': 'tab137',
    'SPECIFIC ACTIVITY': 'tab134'
}


def get_data(ec_no, table_name, html_file=None):
    """
    get data table of enzyme from BRENDA

    :param ec_no: enzyme number (e.g. '1.1.1.1')
    :param table_name: table name (e.g. KM)
    :param html_file: offline file path
    :return: data list
    """
    if html_file:
        html = open(html_file).read()
    else:
        url = 'http://www.brenda-enzymes.org/enzyme.php?ecno=%s' % ec_no
        # todo timeout exception
        html = ''.join(urllib2.urlopen(url))
    print html
    soup = bs(html, 'html.parser')
    tbl = soup.find(id=TABLE_ID[table_name])
    row_list = list()
    for row in tbl.find_all('div', {'class': 'row'}):
        cell_list = row.find_all('div')
        row_list.append([x.strip() for x in map(lambda y: ''.join(y.strings).strip(), cell_list)])
    return row_list




def test():
    ec_no = '1.1.1.1'
    offline_file = '1.1.1.1.html'
    with open('result.csv', 'w') as w:
        for row in get_data(ec_no, 'PATHWAY', offline_file):
            row.append('\n')
            w.write('\t'.join(row).encode('utf-8'))


test()
