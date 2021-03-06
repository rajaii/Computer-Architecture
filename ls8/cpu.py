"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256 #check if correct
        self.register = [0] * 8
        self.pc = 0
        self.SP = 7
        self.register[self.SP] = 0xf4
        self.FL = 0b00000000


    def load(self):
        """Load a program into memory."""
        
        address = 0

        filename = sys.argv[1]
        

        with open(filename) as f:
            for instruction in f:
                instruction = instruction.split('#')
                instruction = instruction[0].strip()
                if instruction == '':
                    continue
                #MAYBE:
                self.ram[address] = int(instruction, 2)
                
                # self.ram[address] = int(instruction, 2)

                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.ram[reg_a] *= self.ram[reg_b]
        elif op == "CMP":
            if reg_a == reg_b:#E flag is true
                self.FL = 0b00000001 
                # print('settilng e flag to true')
            if reg_a != reg_b:
                self.FL = 0b00000000#set e flag to false
                # print('setting e flag to false')
            if reg_a < reg_b:#L flag is true
                self.FL = 0b00000100
            if reg_a > reg_b:#G flag is true
                self.FL = 0b00000010 
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, value):
        self.ram[mar] = value #find out how MDR plays here maybe MDR[value] MDR

    def run(self):
        """Run the CPU."""
        running = True
        HLT = 0b00000001
        ADD = 0b10100000
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101
        CMP = 0b10100111
        

        while running:
            
            
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:#set value of reg to int
                # print('in LDI')
                self.ram_write(operand_a, operand_b)
                self.register[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:#print value stored in given reg
                print(self.register[operand_a])
                self.pc += 2
            elif ir == HLT:
                running = False
                #handle mul case
            elif ir == MUL:
                #call alu passing in params not sure if correct cuz registers not ram
                self.alu("MUL", operand_a, operand_b)
                #increment self.pc
                self.pc += 3
            elif ir == ADD:
                print(f'just added {self.register[operand_a]} and {self.register[operand_a]}')
                self.alu("ADD", operand_a, operand_a)
                
                self.pc += 3           
            elif ir == PUSH:
                #decrement register's value
                prev = self.register[self.SP]
                self.register[self.SP] -= 1
                #take value at register[pc + 1] and add to stack
                reg_num = operand_a
                value = self.register[reg_num] 
                address = self.register[self.SP]
                #self.ram[address] = value
                self.ram_write(address, value)


                #increment pc
                self.pc += 2
            elif ir == POP:
                #copy value from bottom of stack and put in register[pc+1]
            
                value = self.ram[self.register[self.SP]]
                self.ram_write(operand_a, value)
                self.register[operand_a] = value
                #increment stack pointer 
                prev = self.register[self.SP]
                self.register[self.SP] += 1
                
                #increment pc
                self.pc += 2
            elif ir == CALL:
                print('in call')
                return_add = self.pc + 2

                self.register[self.SP] -= 1
                self.ram[self.register[self.SP]] = return_add
                # print(f'just set {self.ram[self.register[self.SP]]} to {return_add}')
                reg_num = operand_a
                dest_addr = self.register[reg_num]

                self.pc = dest_addr
            elif ir == RET:
                print('in ret')
                return_add = self.ram[self.register[self.SP]]
                self.register[self.SP] += 1

                self.pc = return_add
            elif ir == JMP:
                
                reg_num = operand_a
                dest_addr = self.register[reg_num]
                print(f'jumping to {dest_addr} in JMP')
                self.pc = dest_addr
            elif ir == CMP:
                self.alu("CMP", self.register[operand_a], self.register[operand_b])
                # print(f'comparing {self.register[operand_a]} to {self.register[operand_b]}')
                self.pc += 3
            elif ir == JNE:
                if self.FL != 0b00000001:
                    # print('in JNE')
                    reg_num = operand_a
                    dest_addr = self.register[reg_num]
                    # print(f'jumping to {dest_addr} in JNE')
                    self.pc = dest_addr 
                else:
                    self.pc += 2
            elif ir == JEQ:
                if self.FL == 0b00000001:
                    reg_num = operand_a
                    dest_addr = self.register[reg_num]
                    # print(f'jumping to {dest_addr} in JEQ')
                    self.pc = dest_addr 
                else:
                    self.pc += 2
            else:
                print(f'{ir} == unknown command')
                running = False
             



