"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256 #check if correct
        self.register = [0] * 8
        self.pc = 0


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
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        while running:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.ram_write(operand_a, operand_b)
                self.register[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.ram_read(operand_a))
                self.pc += 2
            elif ir == HLT:
                running = False
                #handle mul case
            elif ir == MUL:
                #call alu passing in params not sure if correct cuz registers not ram
                self.alu("MUL", operand_a, operand_b)
                #increment self.pc
                self.pc += 3
            else:
                print('unknown command')
                running = False
             



