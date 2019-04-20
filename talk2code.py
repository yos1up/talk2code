# talk2code.py
import sys
import numpy as np
from io import StringIO

import sys, traceback
def get_error_message(sys_exc_info=None):
    ex, ms, tb = sys.exc_info() if sys_exc_info is None else sys_exc_info
    return '[Error]\n' + str(ex) + '\n' + str(ms) + '\n' + ''.join(traceback.format_tb(tb))


indent_level = 0
stored_code_lines = []

token_list = [
    ['小なりイコール', '≧', '>='],
    ['大なりイコール', '≦', '<='],
    ['ノットイコール', '!='],
    ['イコールイコール', '=='],
    ['プラスイコール', '+='],
    ['マイナスイコール', '-='],
    ['掛けるイコール', '*='],
    ['割るイコール', '/='],
    ['イコール', '='],
    ['小なり', '<'],
    ['大なり', '>'],
    ['かっこ閉じる', 'カッコ閉じる', '括弧閉じる', 'かっことじる', 'カッコとじる', '括弧とじる',
        'かっこ閉じ', 'カッコ閉じ', '括弧閉じ', 'かっことじ', 'カッコとじ', '括弧とじ', '）', ')'],
    ['かっこ', '括弧', '（', '('],
    ['かける', '掛ける', 'X', 'x', '*'],
    ['わる', '割る', 'ワル', '÷', 'スラッシュ', '/'],
    ['パーセント', '％', '%'],
    ['ルート'],
    ['たす', '足す', 'プラス', '+'],
    ['ひく', '引く', 'マイナス', '-'],
    ['カンマ', 'コンマ', ','],
    ['　', ' '],
    ['フォア', 'for'],
    ['リピート', '繰り返し', 'くり返し', 'repeat'],
    ['ループ', 'loop'],
    ['ネクスト', 'next'],
    ['もし', 'イフ', 'if'],
    ['エル水夫', 'elseif', 'elif'],
    ['エルス', 'else'],
    ['ならば', 'then', ':'],
    ['クリアー', 'クリア', 'clear'],
    ['エンド', '終了', 'end'],
    ['プリント', '出力', 'print'],
    ['ブレイク', 'ブレーク', 'break'],
    ['の値を教えて', 'の値を出力して', 'の値を出力', 'を出力して', 'を出力', 'の値は', '^print'],
    # ['文字列終わり', '文字列終端', '"'],
    # ['文字列', '"'],
    # ['ダブルクオート', 'ダブルクォート', '"'],
    # ['クオート', 'クォート', 'quote', "'"],
    ['ディファイン', 'デファイン', 'define', 'def'],
    ['関数定義'],
    ['リターン', 'return'],
    ['レンジ', 'range'],
    ['セミコロン', 'semicolon', '；', ';'],
    ['コロン', 'colon', '：', ':'],
    ['a', 'A'], 
    ['b', 'B'], 
    ['c', 'C'], 
    ['d', 'D'], 
    ['e', 'E'], 
    ['f', 'F'], 
    ['g', 'G'], 
    ['h', 'H'], 
    ['愛', 'i', 'I'], 
    ['j', 'J'], 
    ['k', 'K'], 
    ['l', 'L'], 
    ['m', 'M'], 
    ['n', 'N'], 
    ['o', 'O'], 
    ['p', 'P'], 
    ['q', 'Q'], # 実際は 9 のせいで入力は難しいかもしれない．
    ['r', 'R'], 
    ['s', 'S'], 
    ['t', 'T'], 
    ['u', 'U'], 
    ['v', 'V'], 
    ['w', 'W'], # x は省いてある (かけるの為)
    ['y', 'Y'], 
    ['z', 'Z'],
    ['みどり', '緑'],     
    ['あか', '赤'],     
    ['あお', '青'],     
    ['きいろ', '黄色', '黄'],     
    ['ちゃいろ', '茶色', '茶'],     
    ['くろ', '黒'],     
    ['しろ', '白'],     
    ['むらさき', '紫'],     
    ['ピンク', '桃色', '桃'],     
    ['みずいろ', '水色', '水'],     
    ['こんいろ', '紺色', '紺'],     
    ['きんいろ', '金色', '金'],     
    ['ぎんいろ', '銀色', '銀'],     
    ['みどり', '緑'],     
    ['あか', '赤'],     
    ['あお', '青'],     
    ['きいろ', '黄色', '黄'],     
    ['ちゃいろ', '茶色', '茶'],     
    ['くろ', '黒'],     
    ['しろ', '白'],     
    ['むらさき', '紫'],     
    ['ピンク', '桃色', '桃'],     
    ['みずいろ', '水色', '水'],     
    ['こんいろ', '紺色', '紺'],     
    ['きんいろ', '金色', '金'],     
    ['ぎんいろ', '銀色', '銀'],
]

start_of_string = ['文字列', 'クォート', 'クオート', "'", '"']
end_of_string = ['文字列', 'クォート', 'クオート', "'", '"']



def get_digits(string, start=0):
    # 連続する数字列を頭からとってきて返す（正規表現などに置き換えた方が良いかも？）
    offs = start
    while offs < len(string):
        if not (0 <= ord(string[offs]) - ord('0') <= 9 or string[offs]=='.'):
            break
        offs += 1
    return string[start:offs]



def tokenize(string):
    # 最初にヒットしたものを削り取っていくだけ．
    ret = []
    offs = 0
    while offs < len(string):
        flg = False
        # 文字列の開始の場合
        for s in start_of_string:
            if string[offs:offs+len(s)] == s:
                min_idx, next_idx = len(string), len(string)
                for t in end_of_string:
                    idx = string.find(t, offs+len(s))
                    if idx == -1: idx = len(string)
                    if idx < min_idx:
                        min_idx = idx; next_idx = idx + len(t)
                ret.append("'" + string[offs+len(s):min_idx] + "'")
                offs = next_idx
                flg = True
                break

        # トークンリスト
        for tok in token_list:
            for t in tok:
                if string[offs:offs+len(t)] == t:
                    if tok[-1] != ' ': ret.append(tok[-1]) # スペースはいいや．
                    offs += len(t)
                    flg = True
                    break
            if flg: break
        # 数字列
        digits = get_digits(string, offs)
        if len(digits) > 0:
            ret.append(digits)
            offs += len(digits)
            flg = True
        if not flg: # tokenize 失敗の場合
            return offs # 何文字目で失敗したかを整数値で返す．
    return ret # tokenのリストを返す．


# python に糖衣構文をいっぱいつけたものを目指すか・・・
def resolve_syntax_sugar(tokens):
    delta_indent_level = 0
    if len(tokens) > 0:
        if tokens[0] == 'repeat':
            if len(tokens) >= 3:
                tokens = ['for', tokens[1], 'in', 'range', '(', tokens[2], ')', ':']
            elif len(tokens) == 2:
                tokens = ['for', tokens[1], 'in', 'range', '(', '2147483647', ')', ':']
            elif len(tokens) == 1:
                tokens = ['for', 'i', 'in', 'range', '(', '2147483647', ')', ':']

        if tokens[0] == '関数定義':
            pass


        if tokens[-1] == '^print':
            tokens = ['print', '('] + tokens[:-1] + [')']

        if tokens[0] in ['end', 'next', 'loop']:
            delta_indent_level = -1
            tokens = ['pass']
        
        if tokens[-1] == ':':
            delta_indent_level = +1

    return tokens, delta_indent_level



def process_code(input_code):
    global stored_code_lines, indent_level
    print('[process_code] input_code ==', input_code)
    tokens = tokenize(input_code)
    if isinstance(tokens, int):
        return str(tokens) + '文字目でトークナイズに失敗しました．'
    print('[process_code] tokens ==', tokens)
    tokens, delta_indent_level = resolve_syntax_sugar(tokens)
    print('[process_code] tokens ==', tokens)


    stored_code_lines.append('  ' * indent_level + ' '.join(tokens))
    indent_level += delta_indent_level
    if indent_level == 0: # exec する
        ret = ''
        code_string = '\n'.join(stored_code_lines)
        print('[process_code] code_string ==', code_string)
        the_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        output_string, error_string = '', ''        
        try:
            exec(code_string, globals())
        except:
            error_string = get_error_message()
        sys.stdout = the_stdout
        output_string = redirected_output.getvalue()
        
        # output_string と error_string の内容を ret にまとめる．
        # print('[process_code] output_string ==', output_string)
        # print('[process_code] error_string ==', error_string)
        if error_string == '':
            if output_string == '':
                ret = 'はい．'
            else:
                ret = output_string
        else:
            if output_string == '':
                ret = 'エラーです．' + error_string + ' なお，出力はありません．'
            else:
                ret = 'エラーです．' + error_string + ' また，以下の出力が得られました．' + output_string

        stored_code_lines = [] # 実行したので破棄．
        return ret
    elif indent_level > 0: # インデントが解消されるまで exec しない．
        return 'はい' * (indent_level+1) + '．'
    else:
        return 'これ以上インデントはありません．終了したい場合は「さようなら」と話してください．'




if __name__ == '__main__':
    while 1:
        print(process_code(input()))


