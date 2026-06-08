url_example = "http://dzerp:88/dzerp/aspx/filemanger.aspx?tableid=40&billstate=1&billid=78716"

def generate_urls(bill_start, bill_end, table_ids, bill_states):
    for billid in range(bill_start, bill_end+1):
        for tableid in table_ids:
            for billstate in bill_states:
                yield f"http://dzerp:88/dzerp/aspx/filemanger.aspx?tableid={tableid}&billstate={billstate}&billid={billid}"

for url in generate_urls(1, 10, [11, 40], [1, 2]):
    print(url)