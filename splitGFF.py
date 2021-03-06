#coding=utf-8
__author__ = 'Guoliang Lin'
Softwarename = 'splitGFF'
version = '3.0.1'
data=''
bugfixs = '     2015-12-18:fix some reversed exon\n' \
          '     2016-01-16:spacefy nonconding items\n'
import sys, getopt
import time
def trim(y):
    y = y.replace("[", '')
    y = y.replace(']', '')
    y = y.replace("',", '\t')
    y = y.replace("'", '')
    y = y.replace('\\n', '')
    y = y.replace(' ', '')
    # y=y.replace(',','')
    y = y.strip()
    y = y + '\n'
    return y

def set_to_type(list_item, file,string,genestring,list_type):
    """

    :param listitem:listitem
    :param file:file intergenic or intron
    """
    list_item[2] = string
    list_item[3] = str(min(int(list_type[-2][1]),int(list_type[-1][1])) + 1)
    list_item[4] = str(max(int(list_type[-1][0]),int(list_type[-2][0])) - 1)
    list_item[-1] = genestring
    file.write(trim(str(list_item)))
def convert_to_type(list_item,list_type,file,string,genestring):
    """

    :param list_item: listitem
    :param list_type: ExonsList or GeneList
    :param file: file intergenic or intron
    """
    tmp=list_item[3:5]
    list_type.append(tmp)
    if len(list_type)>2:
        list_type.pop(0)
        set_to_type(list_item,file,string,genestring,list_type)
    elif len(list_type)==2:
        set_to_type(list_item,file,string,genestring,list_type)
ExonsList= []
GenesList=[]
scaffold=''
gene=''
genelist=[]
print('%s software version is %s in 2016-01-19' % (Softwarename, version))
print(bugfixs)
print('starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))

opts, args = getopt.getopt(sys.argv[1:], 'i:t:h', ['inputfile=','type=', 'help'])
InputFileName = ''
for o, a in opts:
    if o in ['-i', '--inputfile']:
        InputFileName = a
    elif o in ['-t','--type']:
        etype=a
#"CDS","exon"
    elif o in ['-h', '--help']:
        help = True
with open(InputFileName, 'r') as InputFile:
    with open(InputFileName+'-'+etype,'w') as cds:
        with open(InputFileName+'-intron','w') as intron:
            with open(InputFileName+'-utr','w') as utr:
                with open(InputFileName+'-intergenic','w') as intergenic:
                    with open(InputFileName+"-noncoding",'w') as nocoding:
                        for item in InputFile:
                            listitem=item.split();
                            if len(listitem)!=0:
                                if scaffold!=listitem[0]:
                                    convert_to_type([scaffold,'.','intergenic',str(sys.maxint),str(sys.maxint),'.','.','.',gene],GenesList,intergenic,'intergenic',gene)
                                    scaffold=listitem[0]
                                    GenesList=[[0,0]]
                                    ExonsList=[]
                                    gene=''
                                if listitem[2]==etype:
                                    cds.write(trim(str(listitem)))
                                elif listitem[2].find('UTR')!=-1:
                                    utr.write(trim(str(listitem)))
                                elif listitem[2]=='gene':
                                    tmpname=gene
                                    gene=listitem[-1]
                                    convert_to_type(listitem,GenesList,intergenic,'intergenic',tmpname+';'+gene)
                                    ExonsList=[]
                                elif listitem[2]=="mRNA":
                                    list1=listitem[:]
                                    if int(listitem[3])>int(GenesList[-1][0]):
                                        listitem[4]=str(int(listitem[3])-1)
                                        listitem[3]=GenesList[-1][0]
                                        listitem[2]="noncodingRNA"
                                        nocoding.write(trim(str(listitem)))
                                    if int(list1[4])<int(GenesList[-1][1]):
                                        list1[3]=str(int(list1[4])+1)
                                        list1[4]=GenesList[-1][1]
                                        list1[2]="noncodingRNA"
                                        nocoding.write(trim(str(list1)))
                                if listitem[2]=='exon':
                                    convert_to_type(listitem,ExonsList,intron,'intron',gene)
                        convert_to_type([scaffold,'.','intergenic',str(sys.maxint),str(sys.maxint),'.','.','.',gene],GenesList,intergenic,'intergenic',gene)
print('ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))
