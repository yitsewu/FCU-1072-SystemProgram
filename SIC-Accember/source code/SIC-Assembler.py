#!/usr/bin/python
# -*- coding: utf-8 -*-

OPCODE = {
    'ADD': '18',
    'AND': '40',
    'COMP': '28',
    'DIV': '24',
    'J': '3C',
    'JEQ': '30',
    'JGT': '34',
    'JLT': '38',
    'JSUB': '48',
    'LDA': '00',
    'LDCH': '50',
    'LDL': '08',
    'LDX': '04',
    'MUL': '20',
    'OR': '44',
    'RD': 'D8',
    'RSUB': '4C',
    'STA': '0C',
    'STCH': '54',
    'STL': '14',
    'STSW': 'E8',
    'STX': '10',
    'SUB': '1C',
    'TD': 'E0',
    'TIX': '2C',
    'WD': 'DC',
}

# SRCFILE
## SRCFILE LOAD
with open('SRCFILE', 'r') as SRCFILE:
    SRCFILE_DATA = []
    while True:
        line = SRCFILE.readline().strip().split()[0:3]
        if not line: break
        if line[0] == '.': continue
        if len(line) < 3: line.insert(0, '')
        SRCFILE_DATA.append(line)

## location Counter Set
if SRCFILE_DATA[0][1] == 'START':
    locationCounter = int('0x' + SRCFILE_DATA[0][2], 16)
else:
    print('ERROR: "START" Not Found')
    exit()

SYMTAB = {'rsub': 0}

for line, index in zip(SRCFILE_DATA, range(0,len(SRCFILE_DATA))):
    SRCFILE_DATA[index].insert(0, hex(locationCounter))

    if line[1] != '':
        if line[1] in SYMTAB:
            print ('Error: Duplicate symbol.')
        else:
            SYMTAB[line[1]] = locationCounter
    
    if line[1].upper() == 'START' or line[1].upper() == 'END': continue
    if line[1].upper() == 'RESB':
        locationCounter += int(line[2])
    elif line[1].upper() == 'RESW':
        locationCounter += int(line[2]) * 3
    elif line[1].upper() == 'BYTE':
        if line[2][0].upper() == 'X':
            locationCounter += int((len(line[2])-3)/2)
        elif line[2][0].upper() == 'C':
            locationCounter += int(len(line[2])-3)
    else:
        locationCounter += 3

## OPCODE
for index, line in enumerate(SRCFILE_DATA):
    obcode = ''
    if line[2].upper() == 'RSUB':
        SRCFILE_DATA[index].append('')
        obcode = '4C0000'
    elif line[2].upper() == 'START' or line[2].upper() == 'END' or line[2].upper() == 'RESW' or line[2].upper() == 'RESB':
        SRCFILE_DATA[index].append(obcode)
        continue
    elif line[2].upper() == 'BYTE':
        if line[3][0].upper() == 'X':
            if len(line[3][2:-1]) % 2 != 0:
                obcode = 'R1'
                SRCFILE_DATA[index].append(obcode)
                continue
            else:
                obcode = line[3][2:-1]
        elif line[3][0].upper() == 'C':
            for char in line[3][2:-1]:
                obcode += str(hex(ord(char))[2:])
    elif line[2].upper() == 'WORD':
        if not line[3].isdigit():
            obcode = 'R2'
            SRCFILE_DATA[index].append(obcode)
            continue
        else:
            obcode = hex(int(line[3]))[2:].zfill(6)
    else:
        if ',x' in line[3]:
            Ctemp = line[3].split(',')
            obcode += OPCODE[line[2].upper()] + str(hex(SYMTAB[Ctemp[0]]+32768)[2:])
        else:
            obcode += OPCODE[line[2].upper()] + str(hex(SYMTAB[line[3]])[2:])            
    SRCFILE_DATA[index].append(obcode)

# LISFILE
with open('LISFILE', 'w') as LISFILE:
    for i in range(len(SRCFILE_DATA)):
        temp = ''
        SRCFILE_DATA[i][0] = SRCFILE_DATA[i][0][2:].zfill(4)
        if SRCFILE_DATA[i][4] == '' or SRCFILE_DATA[i][4][0]=='R':#check if it's a wrong obcode
            LISFILE.write('%s %-6s %-8s %-7s %s\n' %(SRCFILE_DATA[i][0], '', SRCFILE_DATA[i][1], SRCFILE_DATA[i][2], SRCFILE_DATA[i][3]))
            if SRCFILE_DATA[i][4] == 'R1':
                LISFILE.write('**** odd length hex string in byte statement ****\n')
            elif SRCFILE_DATA[i][4] == 'R2':
                LISFILE.write('**** illegal operand in word statement ****\n')
            continue
        elif SRCFILE_DATA[i][2] == 'BYTE' and SRCFILE_DATA[i][3][0] == 'C': #need to change to char
            temp = SRCFILE_DATA[i][0] + ' '
            for j in range(int(len(SRCFILE_DATA[i][4])/2)):
                Ctemp = SRCFILE_DATA[i][4][j*2] + SRCFILE_DATA[i][4][j*2+1] #every chose 2 bit
            temp += '%-6s %-8s %-7s %s' %(chr(int(Ctemp,16)), SRCFILE_DATA[i][1], SRCFILE_DATA[i][2], SRCFILE_DATA[i][3]) #reast of the string
        else:
            temp = '%s %-6s %-8s %-7s %s' %(SRCFILE_DATA[i][0], SRCFILE_DATA[i][4], SRCFILE_DATA[i][1], SRCFILE_DATA[i][2], SRCFILE_DATA[i][3])
        LISFILE.write(temp+'\n')

# OBJFILE
with open('OBJFILE', 'w') as OBJFILE:
    ## Hcard
    ### Hcard = 'H' + ProgramName + ProgramStartAt + ProgramLen (End - Start)
    Hcard = 'H%-6s%s%s' %(SRCFILE_DATA[0][1], SRCFILE_DATA[0][0].zfill(6), hex(int(SRCFILE_DATA[len(SRCFILE_DATA)-1][0],16) - int(SRCFILE_DATA[0][0],16))[2:].zfill(6))
    OBJFILE.write(Hcard.upper()+"\n")

    ## Tcard
    Tcard = ''
    TTEMP = ''
    Tlen = 0
    Ctemp = []
    Error = False

    for i in range(len(SRCFILE_DATA)):
        if Tcard == '' and SRCFILE_DATA[i][4]!= '':
            Tcard += 'T' + SRCFILE_DATA[i][0].zfill(6)
            TTEMP += SRCFILE_DATA[i][4]
            Tlen += int(len(SRCFILE_DATA[i][4])/2)
        elif SRCFILE_DATA[i][2] != 'START':
            if Tlen + int(len(SRCFILE_DATA[i][4])/2) > 30 or SRCFILE_DATA[i][4] == '':
                # 如果長度加現在大於60了，或沒讀到obcode，儲存結束
                Tcard += str(hex(Tlen)[2:]).zfill(2) + TTEMP + '\n'
                if Tcard != '00\n': # 防止印出END
                    OBJFILE.write(Tcard.upper())
                if SRCFILE_DATA[i][2] == 'END':
                    break
                # Reset
                Tcard = ''
                TTEMP = ''
                Tlen = 0
                if SRCFILE_DATA[i][4] != '': # 如果當前有obcode
                    Tcard += 'T' + SRCFILE_DATA[i][0].zfill(6)
                    TTEMP += SRCFILE_DATA[i][4]
                    Tlen += int(len(SRCFILE_DATA[i][4])/2)
                continue
            if SRCFILE_DATA[i][4][1] == 'R': # 有錯誤，直接結束，並且標示不需要E卡片了
                Error == True
                break
            # 以上兩個沒問題，開始放obcode到TTEMP
            if SRCFILE_DATA[i][3][0] == 'C':
                Tlen += int(len(SRCFILE_DATA[i][4])/2)
                if SRCFILE_DATA[i][3][1] == "'":
                    Ctemp = SRCFILE_DATA[i][3].split("'")
                    TTEMP += Ctemp[1]
                else:
                    TTEMP += SRCFILE_DATA[i][4] # 將正確可用的obcode存起來 
            else:
                Tlen += int(len(SRCFILE_DATA[i][4])/2)
                TTEMP += SRCFILE_DATA[i][4] # 將正確可用的obcode存起來

    ## Ecard
    if Error == False:
        Ecard = 'E' + SRCFILE_DATA[0][0].zfill(6)
        OBJFILE.write(Ecard.upper())