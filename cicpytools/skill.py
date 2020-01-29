######################################################################
##        Copyright (c) 2020 Carsten Wulff Software, Norway
## ###################################################################
## Created       : wulff at 2020-1-25
## ###################################################################
##  The MIT License (MIT)
##
##  Permission is hereby granted, free of charge, to any person obtaining a copy
##  of this software and associated documentation files (the "Software"), to deal
##  in the Software without restriction, including without limitation the rights
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##  copies of the Software, and to permit persons to whom the Software is
##  furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included in all
##  copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##  SOFTWARE.
##
######################################################################
import re
import json
import io

class SkillObject:

    def __init__(self,name=""):
        self.name = name
        self.tokens = list()
        self.children = list()
        self.commands = dict()
        self.parent = None
        self.comment = list()

    def addToken(self,token):
        self.tokens.append(token)

    def addComment(self,comment):
        self.comment.append(comment)
        

    def pushList(self):
        g = SkillObject()
        g.parent = self
        self.children.append(g)
        return g

    def pushCommand(self,name):
        g = self.pushList()
        g.name = name
        self.commands[name] = g
        return g

    def toJson(self):
        
        d = dict()

        if self.name:
            d["name"] = self.name


        if len(self.commands) > 0:
            cmd = dict()
            for c in self.commands:
                obj = self.commands[c]
                cmd[c] = obj.toJson()
                d["cmd"] = cmd

        d["tokens"] = self.tokens
        if len(self.comment) > 0:
            d["comment"] = self.comment

        if len(self.children) > 0:
            child = list()
            for obj in self.children:
                child.append(obj.toJson())
                d["children"] = child
        return d


class ReadSkill:

    def __init__(self):
        self.obj = SkillObject()
        self.pointer = self.obj
        self.stack = list()

    def read(self,f):

        isComment = False
        isString = False
        pushToken = False
        buf =  ""
        while True:

            c = f.read(1)

            if not c: break
            
            if c == ';':
                if not isString: isComment = True
            elif not isComment and c == '"':
                isString = not isString
                if not isString:
                    self.pushToken(buf)
                    buf = ""
                    continue
                else: continue
            elif not isString and c == '\n':
                isComment = False
                self.pushComment(buf)
                buf = ""
                continue

            if not( isComment or isString):
                if c == '(':
                    if len(buf) > 0:
                        self.pushCommand(buf)
                    else:
                        self.pushList()
                    buf = ""
                    continue
                elif c == ')':
                    self.pushToken(buf)
                    self.popList()
                    buf = ""
                    continue
                elif c == '\n':
                    self.pushToken(buf)
                    self.popList()
                    buf = ""
                    continue
                elif c.isspace():
                    self.pushToken(buf)
                    buf = ""
                    continue
            isEscape = False
            if c == '\\':
                isEscape = True

            buf += c

    def pushComment(self,comment):
        if re.search(r"^\s*$",comment):
            return
        if self.pointer is None:
            return
        self.pointer.addComment(comment)
        
    def pushToken(self,token):
        if re.search(r"^\s*$",token):
            return
        if self.pointer is None:
            return
        self.pointer.addToken(token)

    def pushList(self):
        if self.pointer is None:
            return
        obj = self.pointer.pushList()
        self.pointer = obj

    def popList(self):
        if self.pointer is None:
            return
        self.pointer = self.pointer.parent

    def pushCommand(self,name):
        if self.pointer is None:
            return
        obj = self.pointer.pushCommand(name)
        self.pointer = obj
        
        
        

def todict(buffer):
    data = dict()

    for c in buf_all:
        print(c)

    return data

def addToken(tokens,tok,c):

    tok = tok.lstrip().rstrip()


    if tok and not tok.isspace():
        tokens.append(tok)

    if not c.isspace() and not c == '"':
        tokens.append(c)

    return ""


def tokenize(f):
    tokens = list()
    tok = ""
    char_ignore = False
    atom = False
    ignore_list = ['\r','\n']
    stack_match = list()
    atoms = {
        '"':'"',
        ';':'\n'
    }
    token_delimiter =  {
        '(' : ')'
    }
    token_delimiter = {**atoms,**token_delimiter}

    ind = 0
    
    while True:
        if isinstance(f,io.IOBase):
            c = f.read(1)
        elif isinstance(f,str):
            if(ind < len(f)):
                c = f[ind]
                ind+=1
            else:
                c = None
        else:
            raise Exception(f"Unknown type '{f}'")
        
        if c is None:
            break

        if char_ignore:
            char_ignore = False
            tok += c
            continue

        if c == r'\\':
            char_ignore = True


        if stack_match and c == stack_match[-1]:
            tok = addToken(tokens,tok,c)
            stack_match.pop()
            atom = False
            continue

        if atom == False and c in token_delimiter:
            if c in atoms:
                atom = True
            stack_match.append(token_delimiter[c])
            tok = addToken(tokens,tok,c)
            continue

        if c in ignore_list:
            continue

        tok += c

    return tokens



def read_tokens(tokens):

    ind = 0
    atoms = ['(',')','"','"']

    # Try to figure out whether this level is a dict or list
    # A dict will start with <key>(, while a list will start with ( <key>)
    # First I need to remove comments
    while(tokens[0] == ';'):
        tokens.pop(0)
        tokens.pop(0)

    isdict = False
    data = list()
    if(tokens[0] != '"' and tokens[1] == '('):
        print(tokens[0] + " " + tokens[1])
        data = dict()
        isdict = False

    prev_tok = ""
    key = ""
    while(ind >= 0):
        if not tokens:
            break

        tok = tokens.pop(0)

        if not tok:
            continue

        if tok == ';':
            tokens.pop(0)
            continue


        if(tokens[0] == '('):
            key = tok
            continue

        if tok == '"':
            tok = tokens.pop(0)
            tokens.pop(0) # Pop the ending " also


        if(tok == '('):
            ind+=1
            if key and isinstance(data,dict):
                data[key] = read_tokens(tokens)
            elif isinstance(data,dict):
                raise Exception("Ops, data is dict without key tok:'" + tok + "' key:'"+key+"'")
            else:
                data.append(read_tokens(tokens))

        elif(tok == ')'):
            ind-=1
            key = ""
            break
        else:
            if isinstance(data,dict):
                raise Exception("Ops, data is dict without key tok:'" + tok + "' key:'"+key+"'")
            else:
                data.append(tok)



        prev_tok = tok

    return data

def read_data(buffer):

    if not buffer:
        return
    
    if not buffer[0].startswith(";"):
#        print(f"INFO: don't know how to parse this buffer '{buffer}'")
        return

    header = buffer[0].replace(";","")
    print(header)
    htok = tokenize(header)
    print(htok)
        


def read(f,level,pkey=""):
    data = dict()
    buf = list()
    for line in f:

        
        if(level < 1 and re.search(r"^\s*;",line)):
            continue
        if(re.search(r"^\s*$",line)):
            continue
        
        if( level > 0 and re.search(r"^\s*\)\s+;" + pkey,line)):
            read_data(buf)
            #data["buffer"] = buf
            return data
        
        m = re.match(r"^\s*(\w+)\(([^\)]+)?\)?",line)
        if m:
            key = m.groups()[0]
            val = m.groups()[1]
            if val and not val.isspace():
                data[key] = val.lstrip("\"").rstrip("\"")
            else:
                level += 1
                data[key] = read(f,level,pkey=key)
            continue

        buf.append(line.lstrip().rstrip())
        
    return data


def parse(file_tf):

    r = ReadSkill()
    with open(file_tf,"r") as f:
        #data = read(f,0)
        r.read(f)

    return r.obj

#    print(json.dumps(r.obj.toJson(),indent=4))
#    print(json.dumps(data,indent=4))
