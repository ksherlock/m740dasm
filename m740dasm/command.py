'''
Usage: m740dasm <filename.bin>

'''

import sys

from m740dasm.disasm import disassemble_inst
from m740dasm.trace import Tracer
from m740dasm.memory import Memory
from m740dasm.listing import Printer
from m740dasm.symbols import M3886_SYMBOLS, M50740_SYMBOLS, SymbolTable

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(__doc__)
        sys.exit(1)

    with open(sys.argv[1], 'rb') as f:
        rom = bytearray(f.read())
    # start_address = 0x10000 - len(rom)
    start_address = 0x2000 - len(rom)
    memory = Memory(rom)

    # entry_points = [0xa4d1]
    entry_points = []

    vectors = [
        # brk
        #0xffdc,
        # interrupts
        #0xffde, 0xffe0, 0xffe2, 0xffe4, 
        #0xffe6, 0xffe8, 0xffea, 0xffec,
        #0xffee, 0xfff0, 0xfff2, 
        0xfff4, 0xfff6, 0xfff8, 0xfffa,
        # reset
        0xfffc, 0xfffe
    ]

    vectors = [x & 0x1fff for x in vectors]

    traceable_range = range(start_address, start_address + len(rom) + 1)
    tracer = Tracer(memory, entry_points, vectors, traceable_range)
    tracer.trace(disassemble_inst)

    symbol_table = SymbolTable(M50740_SYMBOLS)  #M3886_SYMBOLS)
    symbol_table.generate(memory, start_address) # xxx should pass traceable_range

    printer = Printer(memory,
                      start_address,
                      symbol_table,
                      )
    printer.print_listing()


if __name__ == '__main__':
    main()
