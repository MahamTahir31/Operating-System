class Process:
    counter = 0

    def __init__(self, processId, executionTime):
        Process.counter += 1
        self.processId = processId
        self.resume = 1
        self.executionTime = executionTime
        self.executed = 0
        self.isexecuted = False
        self.state = 'R'
        self.resource = False


class PCB:
    def __init__(self, NProcess, Quantumsize, Executiontime):
        self.nprocess = NProcess
        self.quantumsize = Quantumsize
        self.processlist = []
        self.IR = 0
        self.PC = 0

        for i in range(self.nprocess):
            tempprocess = Process(i + 1, Executiontime[i])
            self.processlist.append(tempprocess)
        


        self.roundrobin()

    def roundrobin(self):
        while not self.isallexecute():
            if not self.processlist[self.PC].isexecuted:
                currentprocess = self.processlist[self.PC]

                if currentprocess.executed == currentprocess.executionTime - 2:
                    currentprocess.resource = True

                if currentprocess.resource:
                    currentprocess.state = 'B'
                    currentprocess.executed += 1
                    self.IR = currentprocess.resume
                    self.PC = self.assignPC(self.PC)
                    currentprocess.resume += 1
                    self.printPCB(currentprocess, 1)
                    currentprocess.state = 'R'
                    currentprocess.resource = False
                else:
                    rem = currentprocess.executionTime - currentprocess.executed
                    if rem <= self.quantumsize:
                        self.IR = currentprocess.resume + rem - 1
                        currentprocess.executed = currentprocess.executionTime
                        currentprocess.resume = -1
                        self.PC = self.assignPC(self.PC)
                        self.printPCB(currentprocess, rem)
                        currentprocess.isexecuted = True
                    else:
                        self.IR = currentprocess.resume + self.quantumsize - 1
                        self.PC = self.assignPC(self.PC)
                        currentprocess.resume += self.quantumsize
                        currentprocess.executed += self.quantumsize
                        self.printPCB(currentprocess, self.quantumsize)

    def assignPC(self, processId):
        i = (processId + 1) % self.nprocess
        while True:
            if not self.processlist[i].isexecuted:
                return i
            else:
                i = (i + 1) % self.nprocess
                if i == processId and not self.processlist[i].isexecuted:
                    return i
        return -1

    def isallexecute(self):
        for i in range(self.nprocess):
            if not self.processlist[i].isexecuted:
                return False
        return True

    def printPCB(self, myprocess, QT):
       
        if not myprocess.isexecuted:
            print(f"\t\t\t\t\t\t\t\t=========PCB of process {myprocess.processId}========")
            print("\t\t\t\t\t\t\t\tScheduling Algorithm: Round Robin")
            print(f"\t\t\t\t\t\t\t\tQuantum size = {QT}")
            print(f"\t\t\t\t\t\t\t\tExecution time = {myprocess.executionTime}")
            print(f"\t\t\t\t\t\t\t\tValue of PC: process {self.PC + 1} = [{self.processlist[self.PC].resume}]")

            if myprocess.resource:
                print(f"\t\t\t\t\t\t\t\tResource required at process {myprocess.processId} = [{self.IR}]")
            else:
                print(f"\t\t\t\t\t\t\t\tValue of IR = process {myprocess.processId} = [{self.IR}]")
                print("\t\t\t\t\t\t\t\tExecuted = [", end="")
                for i in range(myprocess.executed):
                    print(i + 1, end="")
                    if i < myprocess.executed - 1:
                        print(",", end="")
                print("]")
                print("\t\t\t\t\t\t\t\tRemaining = [", end="")
                for i in range(myprocess.executed, myprocess.executionTime):
                    print(i + 1, end="")
                    if i < myprocess.executionTime - 1:
                        print(",", end="")
                print("]")
            print(f"\t\t\t\t\t\t\t\tWill resume from process {myprocess.processId} = [{myprocess.resume}]")
            if myprocess.state == 'R' and not myprocess.resume == -1:
                print("\t\t\t\t\t\t\t\tState = Running\n\t\t\t\t\t\t\t\t=================================\n")
            elif myprocess.resume == -1:
                print("\t\t\t\t\t\t\t\tState = Terminated\n\t\t\t\t\t\t\t\t=================================\n")
            else:
                print("\t\t\t\t\t\t\t\tState = Blocked\n\t\t\t\t\t\t\t\t=================================\n")
                

def main():
    process = 0
    execution = 0
    quantumsize = 0

    while process < 3 or process > 5:
        process = int(input("How many processes you want to run? (3-5): "))

    executiontime = []
    for i in range(process):
        while execution < 1 or execution > 10:
            execution = int(input(f"Enter execution time of process {i + 1}: (1-10): "))
        executiontime.append(execution)
        execution = 0

    while quantumsize < 1 or quantumsize > 3:
        quantumsize = int(input("Enter your quantum size: (1-3): "))

    mypcb = PCB(process, quantumsize, executiontime)


if __name__ == "__main__":
    main()
