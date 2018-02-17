from lib.analysis.author.wh_table import *


def test_generate_wh_table_authors():

    nodelist_filename = './test/integration_test/data/graph_nodes.csv'
    edgelist_filename = './test/integration_test/data/graph_edges.csv'
    output_filename = './test/integration_test/data/wh_table_authors.csv'

    req_file_data1 = """Height(h),Number of authors(i)
 ,1,,2,,3,,4,,5,,6,,7,,8,,9,,10,,11,,12,,13,,14, ,Subtotal
 ,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New
0,1530,1530,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1530
1,865,832,230,192,42,21,6,5,2,2,2,3,1,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0,1151
2,589,267,152,45,26,4,6,3,6,1,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,781
3,384,166,135,26,19,7,4,1,5,0,1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,550
4,298,98,80,13,17,4,2,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,401
5,208,69,47,8,13,1,3,1,3,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,276
6,151,42,32,3,9,2,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,196
7,100,30,21,4,8,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,132
8,77,17,13,0,2,1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,94
9,45,13,10,0,3,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,60
10,32,4,2,3,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,41
11,18,3,7,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,27
12,12,3,3,1,3,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20
13,10,2,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13
14,7,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11
15,8,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9
16,5,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7
17,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4
18,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4
19,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3
20,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3
21,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2
22,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
Total:,5316
"""

    req_file_data2 = """Height(h),Number of authors(i)
 ,1,,2,,3,,4,,5,,6,,7,,8,,9,,10,,11,,12,,13,,14, ,Subtotal
 ,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New,Total,New
0,1093,1093,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1093
1,807,832,230,192,42,21,6,5,2,2,2,3,1,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0,1093
2,581,267,152,45,26,4,6,3,6,1,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,773
3,381,166,135,26,19,7,4,1,5,0,1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,547
4,297,98,80,13,17,4,2,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,400
5,207,69,47,8,13,1,3,1,3,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,275
6,151,42,32,3,9,2,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,196
7,100,30,21,4,8,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,132
8,77,17,13,0,2,1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,94
9,45,13,10,0,3,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,60
10,32,4,2,3,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,41
11,18,3,7,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,27
12,12,3,3,1,3,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20
13,10,2,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13
14,7,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11
15,8,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9
16,5,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7
17,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4
18,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4
19,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3
20,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3
21,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2
22,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
Total:,4808
"""

    generate_wh_table_authors(nodelist_filename, edgelist_filename, output_filename)
    #print(generate_wh_table_authors(nodelist_filename, edgelist_filename, output_filename))
    with open(output_filename, 'r') as wh_table_file:
        wh_table_data = wh_table_file.read()
        assert wh_table_data == req_file_data1
    #print(generate_wh_table_authors(nodelist_filename, edgelist_filename, output_filename, ignore_lat=True))
    generate_wh_table_authors(nodelist_filename, edgelist_filename, output_filename, ignore_lat=True)

    with open(output_filename, 'r') as wh_table_file:
        wh_table_data = wh_table_file.read()
        assert wh_table_data == req_file_data2

