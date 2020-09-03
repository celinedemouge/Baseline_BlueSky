

class ScenarioCreator:
    def __init__(self):
        self.nbAicraft = 0
        self.IAF = []
        self.RWY = ""
    def create(self):
        rwy = input("Which RWY do you want to use ?")
        print("You have choosen RWY {}".format(rwy))
        self.RWY = rwy
        
        n = int(input("How many aircraft ?"))
        self.nbAircraft = n
        print("You have requested {} aircraft.".format(n))
        
        for i in range(n):
            iaf = input("Which iaf for aircraft number {} ?".format(i))
            self.IAF.append(iaf)
            print("You have requested iaf {} for aircraft {}".format(iaf,i))

    def createScenarioFile(self):
        if self.RWY == "02":
            self.createScenarioFile02()
        elif self.RWY in ["07R","07L"]:
            self.createScenarioFile07()
        elif self.RWY in ["25R","25L"]:
            self.createScenarioFile25()
        else:
            print("This RWY doesn't exist")
        

    def createScenarioFile02(self):
        with open("results/result02.scn",'w') as f:
            print('hello')
            for i in range(self.nbAircraft):
                ac = "AC000{}".format(i+1)
                if self.IAF[i] == "TOTKI" :
                    f.write("\n")
                    f.write("00:00:01.11>CRE,{0},A320,40.785860,0.593547,030,25000,250".format(ac))
                    f.write("\n")
                    
                    f.write("00:00:01.11>DEFWPT,BL636,41.0533,1.8825")
                    f.write("\n")
                    f.write("00:00:01.11>DEFWPT,TOTKI,41.1333,1.7308")
                    f.write("\n")
                    f.write("00:00:01.11>ADDWPT,{0},TOTKI,7000,220".format(ac))

                    f.write("\n")
                    f.write("00:00:02.11>ADDWPT,{0},41.1164,1.9111,5000,220".format(ac))

                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{0},BL636,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.11>LNAV {0} ON".format(ac))
                    f.write("\n")
                    f.write("00:00:01.11>VNAV {0} ON".format(ac))
                else :
                    f.write("\n")
                    f.write("00:00:01.11>CRE,{0},A320,41.383340,5.675410,260,25000,250".format(ac))
                    f.write("\n")
                    f.write("00:00:01.11>ADDWPT,{0},VIBIM,7000,220".format(ac))
                    f.write("\n")

                    f.write("00:00:02.11>ADDWPT,{0},41.0719,2.0822,5000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL635,41.0089,2.0536")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{0},BL635,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.11>LNAV {0} ON".format(ac))
                    f.write("\n")
                    f.write("00:00:03.11>VNAV {0} ON".format(ac))

    def createScenarioFile07(self):
        filename = "results/result{}.scn".format(self.RWY)
        with open(filename,'w') as f:
            
            for i in range(self.nbAircraft):
                ac = "AC000{}".format(i+1)
                f.write("\n")
                if self.IAF[i] == "VLA" :
                    f.write("00:00:01.11>CRE,{},A320,40.904147,-1.206067,090,25000,250".format(ac))
                    f.write("\n")
                    f.write("00:00:01.11>ADDWPT,{},VLA,7000,220".format(ac))
                    f.write("\n")

                    f.write("00:00:02.05>ADDWPT,{},41.34,1.7192,5000,220".format(ac))
                    f.write("\n")

                    f.write("00:00:02.11>ADDWPT,{},41.2642,1.7647,5000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL537,41.2367,1.6844")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL537,,220".format(ac))
                    f.write("\n")

                elif self.IAF[i] == "SLL" :
                    f.write("00:00:01.11>CRE,{},A320,43.0661,-0.306,260,25000,250".format(ac))

                    f.write("\n")


                    f.write("00:00:01.11>ADDWPT,{},SLL,7000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:02.05>ADDWPT,{},41.34,1.7192,5000,220".format(ac))
                    f.write("\n")

                    f.write("00:00:02.11>ADDWPT,{},41.2642,1.7647,5000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL537,41.2367,1.6844")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL537,,220".format(ac))
                    f.write("\n")
                    
                elif self.IAF[i] == "VIBIM" :
                    f.write("00:00:01.11>CRE,{},A320,41.1442,5.1845,270,25000,250".format(ac))
                    f.write("\n")



                    f.write("00:00:01.11>ADDWPT,{},VIBIM,7000,220".format(ac))
                    f.write("\n")

                    f.write("00:00:02.05>ADDWPT,{},41.0639,1.8853,5000,220".format(ac))
                    f.write("\n")

                    f.write("00:00:02.11>ADDWPT,{},41.1397,1.8397,5000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL538,41.1122,1.7594")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL538,,220".format(ac))
                    f.write("\n")


                    
                elif self.IAF[i] == "RUBOT" :
                    f.write("00:00:01.11>CRE,{},A320,40.904147,-1.206067,090,25000,250".format(ac))
                    f.write("\n")
                    
                    f.write("00:00:01.11>ADDWPT,{},RUBOT,7000,220".format(ac))
                    f.write("\n")

                    f.write("00:00:02.05>ADDWPT,{},41.0639,1.8853,5000,220".format(ac))
                    f.write("\n")
                    
                    f.write("00:00:02.11>ADDWPT,{},41.1397,1.8397,5000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL538,41.1122,1.7594")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL538,,220".format(ac))




                    
                f.write("\n")
                f.write("00:00:03.11>LNAV {0} ON".format(ac))
                f.write("\n")
                f.write("00:00:03.11>VNAV {0} ON".format(ac))

    def createScenarioFile25(self):
        filename = "results/result{}.scn".format(self.RWY)
        with open(filename,'w') as f:
            
            for i in range(self.nbAircraft):
                ac = "AC000{}".format(i+1)
                if self.IAF[i] == "CLE" :
                    f.write("\n")
                    f.write("00:00:01.11>CRE,{},A320,42.422717,1.92291,170,30000,250".format(ac))
                    f.write("\n")

                    f.write("00:00:01.11>ADDWPT,{},CLE,7000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:01.11>ADDWPT,{},41.52388,2.25833,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:02.11>ADDWPT,{},41.44805,2.304167,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL435,41.4756,2.385,FIX")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL435,5000".format(ac))
                    f.write("\n")

                elif self.IAF[i] == "SLL" :
                    f.write("\n")
                    f.write("00:00:01.11>CRE,{},A320,42.422717,1.92291,170,30000,250".format(ac))
                    f.write("\n")

                    f.write("00:00:01.11>ADDWPT,{},SLL,7000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:01.11>ADDWPT,{},41.52388,2.25833,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:02.11>ADDWPT,{},41.44805,2.304167,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL435,41.4756,2.385,FIX")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL435,5000".format(ac))
                    f.write("\n")
                    
                elif self.IAF[i] == "LESBA" :
                    f.write("\n")
                    f.write("00:00:01.11>CRE,{},A320,40.7958,2.5683,005,19000,250".format(ac))
                    f.write("\n")

                    f.write("00:00:01.11>ADDWPT,{},LESBA,7000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:01.11>ADDWPT,{},41.2475,2.4247,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:02.11>ADDWPT,{},41.3233,2.379167,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL436,41.3508,2.4597")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL436,5000".format(ac))
                    f.write("\n")
                    
                elif self.IAF[i] == "RULOS" :
                    f.write("\n")
                    f.write("00:00:01.11>CRE,{},A320,40.7958,2.5683,005,19000,250".format(ac))
                    f.write("\n")

                    f.write("00:00:01.11>ADDWPT,{},RULOS,7000,220".format(ac))
                    f.write("\n")
                    f.write("00:00:01.11>ADDWPT,{},41.2475,2.4247,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:02.11>ADDWPT,{},41.3233,2.379167,,220".format(ac))
                    f.write("\n")
                    f.write("00:00:03.05>DEFWPT,BL436,41.3508,2.4597")
                    f.write("\n")
                    f.write("00:00:03.11>ADDWPT,{},BL436,5000".format(ac))
                    f.write("\n")
                    
                    
                f.write("\n")
                f.write("00:00:03.11>LNAV {0} ON".format(ac))
                f.write("\n")
                f.write("00:00:03.11>VNAV {0} ON".format(ac))

                    

def main():
    creator = ScenarioCreator()
    creator.create()
    creator.createScenarioFile()

if __name__=="__main__":
    main()
                            
                    
            
        
    
