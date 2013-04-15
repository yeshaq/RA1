import sys, getopt

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

def main(argv):
   inputfile = ''
   outputfile = ''
   assert len(sys.argv) > 1, "Expected input JSON file, proper usage: splitJSONInOddAndEven.py -i <inputfile>'"
   
   try:
       opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
       print 'splitJSONInOddAndEven.py -i <inputfile>'
       sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'splitJSONInOddAndEven.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   f = open(inputfile, "r")
   searchlines = f.readlines()
   assert len(searchlines) > 1, "This script was made for DCSONLY JSON which are not one line long"
   f.close()
   oddFile = open("odd_%s"%inputfile,"w")
   evenFile = open("even_%s"%inputfile,"w")
   even = int(1)
   evenFile.write("{\n")
   oddFile.write("{\n")
   print 1*"\n"
   print "Starting to split %s in odd and even files"%f.name
   print 10*"-------"
   for i, line in enumerate(searchlines):
       if i == 0 : continue 
       if "\"" in line:
           if int(line[line.find("\"")+1:line.rfind("\"")])%2 == 0 : ## parses run number
               even = 1
               evenFile.write(line)
           else : 
               even = 0
               oddFile.write(line)
       else:
           if even == 1:
               evenFile.write(line)
           else : oddFile.write(line)

   oddFile.close()
   evenFile.close()        

   print "%s has been created"%oddFile.name
   print "%s has been created"%evenFile.name
   print 5*"-------"
   checkScript(open("odd_%s"%inputfile,"r"))
   checkScript(open("even_%s"%inputfile,"r"))


def checkScript(f):
    print "Now Checking %s"%f.name
    print 5*"---"
    searchlines = f.readlines()
    for i, line in enumerate(searchlines):    
        if "\"" in line :
            if "even" in f.name : 
                assert int(line[line.find("\"")+1:line.rfind("\"")])%2 == 0, "ERROR: Odd numbered run found in %s, line %i"%(f.name,i)
            else :
                assert int(line[line.find("\"")+1:line.rfind("\"")])%2 == 1, "ERROR: Even numbered run found in %s, line %i"%(f.name,i)
    if "even" in f.name:
        print "All run numbers in %s are even"%f.name
    else :    
        print "All run numbers in %s are odd"%f.name
    print "\nDone\n"


if __name__ == "__main__":
   main(sys.argv[1:])
