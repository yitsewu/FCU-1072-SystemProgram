# SIC-Assembler 報告

[TOC]

## 學號、姓名
- D0618990 巫逸哲
## ilearn 需求
- [x] source code
- [x] executable code
- [x] sample assembly program

## 開發語言及平台
- 本次使用 Python 作為開發語言
- 本次使用 Visual Studio Code 平台開發
- 簡述：
    - 相較於 C 及 JAVA 等其它語言，Python 在處理字串及檔案讀寫有提供方便的FUNCTION可以呼叫，在程式邏輯編寫上也更加簡潔，降低錯誤機率。
    - 而 Visual Studio Code 為微軟開發之文字編輯器，因有整合終端機介面，且相關輔助套件（高亮、錯誤資訊提示...），開發非常便利。

## 格式輸入
- 需要組譯的檔案名稱須為 "SRCFILE" (尚未做到任意檔名兼容)
- 內容格式：一般SIC組合語言程式格式
- 附註：目前可支援包含註解之組合語言程式

## Assembler Directives
- 可正常處理的組譯器假指令
    - start, end, resw, resb, word, byte
- 即 SIC 基本版假指令皆可執行

## Data Structures
- 說明 PASS_1 程式內所用變數之功能：
    - OPCODE：存放指令之 opcode，型態為字典
    - locationCounter：計算個指令記憶體位址的站存變數
    - SRCFILE_DATA：整個 SRCFILE 之內容。於之後會逐一編寫位址及Object code。
    - SYMTAB 紀錄標籤位址
- 說明 PASS_2 程式內所用變數之功能：
    - obcode：依各種指令編寫 object code 時所用到的暫存
    - Ctemp：當讀到BYTE且變數為C' '時，將規定之存入 Ctemp
## 程式流程
- SRCFILE
    - LOAD SRCFILE
    - Set location Counter
    - Set Object code
- LISFILE
    - Attend or Insert location Counter and Object code
    - Write LISFILE
- OBJFILE
    - Hcard
         'H' + ProgramName + ProgramStartAt + ProgramLen (End - Start)
    - Tcard
        為string型態，最後會將成功的T卡片寫入FILE內
        若是有失敗的T卡片，會將程式結束，並提醒之後的E卡片不需要做
    - Ecard

## 心得
恩，十分難得的體驗，在寫的當中得不斷去思考各種去能性。
程式歷經了好多次改版，且因為一開始的嘗試加上變數名亂取，造成後續優化非常好時。
且程式出錯也讓人非常難以修正，且寫文件時也變得不易撰寫。
由這次學到了要好好的規劃撰寫。

## 參考文獻
- 說明：全部僅都參考架構而已，程式部分都是自行設計。
- Python 各式使用方式
    - Google
- GitHub 專案
    - andy6804tw：https://github.com/andy6804tw/SIC.git
    - amritkrs：https://github.com/amritkrs/SIC-ASSEMBLER.git
    - travcunn：https://github.com/travcunn/sic_assembler.git
    - ......
    - toyraynei：https://github.com/toyraynei/System_Program.git

## 備註：
本專案有放置在 GitHub 上
連結：https://github.com/yitsewu1998/SIC-Accember.git
