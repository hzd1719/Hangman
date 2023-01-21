import wx
import string
import random
import sys
#import time

#list of all the alpabet
#alpha_cyr = "А,Б,В,Г,Д,Е,Ё,Ж,З,И,Й,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Ш,Щ,Ъ,Ы,Ь,Э,Ю,Я"
#alpha_cyr  = alpha_cyr.split(',')

alpha = list(string.ascii_uppercase)
#alpha = alpha_cyr
alpha_size = len(alpha)
#Optional
arr = []
words = []
for arg in sys.argv:
    arr.append(arg)
file = "words.txt"
f = open(file)
for line in f:
    words.append(line[0:-1].upper())

#words = ["ТЕСТ"]
#words = ["SSMRSADD SAD"]
words_copy = words.copy()

class Hangman(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(Hangman, self).__init__(*args, **kw)
        
        #choosing random word
        self.word = random.choice(words_copy)
        #w.remove(self.word)
        
        #if words_copy is empty fill it again 
        if not words_copy:
            for i in words:
                words_copy.append(i)
            
        self.n = 2
        #sz is the length of the word - 2(first letter and last letter)
        self.sz = len(self.word) - self.n
        self.tries = 6
        

        self.font = wx.Font(alpha_size, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.pnl = wx.Panel(self)
        self.hangman = wx.Bitmap('1hang_small.png',
wx.BITMAP_TYPE_PNG)
        self.img=wx.StaticBitmap(self.pnl, 0, self.hangman,
            pos=(220,250))
        

        self.heading = wx.StaticText(self.pnl, label = "", pos = (200, 390))
        self.heading.SetLabel("You have {} tries left".format(self.tries))
        self.heading.SetFont(self.font)
        #the word to be guessed(show the first and last letter) and which is being displayed
        self.guess_word = [""]
        for i in range(1, len(self.word)):
            if(self.word[i] == self.word[0]):
                self.guess_word.append(self.word[0] + " ")
            elif(self.word[i] == self.word[-1]):
                self.guess_word.append(self.word[-1] + " ")
            elif(self.word[i] == " "):
                self.guess_word.append("  ")
            else:
                self.guess_word.append("_ ")
        self.guess_word[0] = self.word[0] + " "
        self.guess_word[-1] = self.word[-1]
        self.guess_word = "".join(self.guess_word)
        #self.guess_word = self.word[0] + " " + self.sz*"_ " + self.word[-1] + " "
        #display the word
        self.hang = wx.StaticText(self.pnl, label = self.guess_word, pos = (220, 10))
        self.hang.SetFont(self.font)
        
        #list of all buttons as objects
        self.buttons = []
        #dictionary with all the letters and if they have already been used by the user
        self.pressed_buttons = {}
        
        m = 120
        n = 80
        j = 0
        for i in range((alpha_size)):
            #fill and display the list of all buttons as objects
            self.buttons.append(wx.ToggleButton(self.pnl, label = alpha[i], pos = ((n + j*20, m)), size = wx.Size((30, 30))))
            #on initiliaze none letters are used by the yser
            self.pressed_buttons[alpha[i]] = False
            #position the buttons
            j +=2
            if i == 10 or i == 21:
                n = 80
                m += 35
                j = 0
        for i in range(alpha_size):
            self.buttons[i].Bind(wx.EVT_TOGGLEBUTTON, self.Check)
            if self.buttons[i].GetLabel() == self.word[0]:
                self.buttons[i].Disable()
                self.pressed_buttons[self.word[0]] = True
            if self.buttons[i].GetLabel() == self.word[-1]:
                self.buttons[i].Disable()
                self.pressed_buttons[self.word[-1]] = True
        
        self.InitUI()


    def InitUI(self):
        self.SetSize((600, 480))
        self.SetTitle('Hangman')
        self.Centre()
        self.Show(True)
    def Reset(self,e):
        try:
            self.word = random.choice(words_copy)
        except:
            for i in words:
                words_copy.append(i)
            self.word = random.choice(words_copy)
        
       
        self.n = 2
        self.sz = len(self.word) - self.n
        self.tries = 6
        self.guess_word = [""]
        for i in range(1, len(self.word)):
            if(self.word[i] == self.word[0]):
                self.guess_word.append(self.word[0] + " ")
            elif(self.word[i] == self.word[-1]):
                self.guess_word.append(self.word[-1] + " ")
            elif(self.word[i] == " "):
                self.guess_word.append("  ")
            else:
                self.guess_word.append("_ ")
        self.guess_word[0] = self.word[0] + " "
        self.guess_word[-1] = self.word[-1]
        self.guess_word = "".join(self.guess_word)
        #self.guess_word = self.word[0] + " " + self.sz*"_ " + self.word[-1] + " "
        for i in range(alpha_size):
            self.pressed_buttons[alpha[i]] = False
            self.buttons[i].Enable()
            self.buttons[i].SetValue(False)
            if self.buttons[i].GetLabel() == self.word[0]:
                self.buttons[i].Disable()
                self.pressed_buttons[self.word[0]] = True
            if self.buttons[i].GetLabel() == self.word[-1]:
                self.buttons[i].Disable()
                self.pressed_buttons[self.word[-1]] = True
        self.heading.SetLabel(" ")
        self.heading.SetLabel("You have {} tries left".format(self.tries))
        self.hang.SetLabel(self.guess_word)
        self.hangman.LoadFile("1hang_small.png", wx.BITMAP_TYPE_PNG)
        self.img.SetBitmap(self.hangman)
        self.rbtn.Disable()
        self.rbtn.Hide()

    def Check(self,e):
        #get the pressed_buttons letter
        obj = e.GetEventObject()
        #disable the letter so the user can't use it again
        obj.Disable()
        #take the letter as a string
        strn = obj.GetLabel()
        #make the letter upper case
        strn = strn.upper()
        
        #if the user has guessed correctly that the letter is in the word
        if strn in self.word:
            self.sz = self.sz - 1
            guess_word_ls = [""] * len(self.guess_word)
            for i in range(0, len(self.guess_word)):
                guess_word_ls[i] = self.guess_word[i] 
            
            new_word_ls = [""] * len(self.guess_word)
            
            j = 0
            for i in range(0, len(self.word)-1):
                if(self.word[i] != strn):
                    new_word_ls[j] = guess_word_ls[j]
                    new_word_ls[j+1] = guess_word_ls[j+1]
                   
                else:
                    new_word_ls[j] = strn
                    new_word_ls[j+1] = " "
                j = j + 2
                    
            new_word_ls[-2] = guess_word_ls[-2]
            new_word_ls[-1] = guess_word_ls[-1]
            #new_word = [i for i in new_word if i != " "]
            new_word_str = "".join(new_word_ls)
            self.guess_word = new_word_str
            print(self.guess_word)
            guess_word_stripped = self.guess_word.replace(" ", "");
            print(guess_word_stripped)
            self.hang.SetLabel(new_word_str)
            
            if guess_word_stripped == self.word.replace(" ", ""):
                self.heading.SetLabel("You have won!")
                words_copy.remove(self.word)
                self.rbtn = wx.Button(self.pnl, label='Reset', pos=(250, 75))
                self.rbtn.Bind(wx.EVT_BUTTON, self.Reset)
                for i in range(0, 26):
                    self.buttons[i].Disable()
        
        #if the user has guessed incorrectly
        else:
            #if the user haven't already tried with that letter
            if self.pressed_buttons[strn] == False:
                self.tries = self.tries - 1
                if self.tries == 5:
                    self.hangman.LoadFile("2head_small.png", wx.BITMAP_TYPE_PNG)
                    self.img.SetBitmap(self.hangman)
                if self.tries == 4:
                    self.hangman.LoadFile("3body_small.png", wx.BITMAP_TYPE_PNG)
                    self.img.SetBitmap(self.hangman)
                if self.tries == 3:
                    self.hangman.LoadFile("4handleft_small.png", wx.BITMAP_TYPE_PNG)
                    self.img.SetBitmap(self.hangman)
                if self.tries == 2:
                    self.hangman.LoadFile("5bothhands_small.png", wx.BITMAP_TYPE_PNG)
                    self.img.SetBitmap(self.hangman)
                if self.tries == 1:
                    self.hangman.LoadFile("6legleft_small.png", wx.BITMAP_TYPE_PNG)
                    self.img.SetBitmap(self.hangman)
                if self.tries == 0:
                    self.hangman.LoadFile("7hangman_small.png", wx.BITMAP_TYPE_PNG)
                    self.img.SetBitmap(self.hangman)

            if self.tries > 0:
                self.heading.SetLabel("You have {} tries left".format(self.tries))
            else:
                self.heading.SetLabel("   Game Over!")
                self.rbtn = wx.Button(self.pnl, label='Reset', pos=(250, 75))
                self.rbtn.Bind(wx.EVT_BUTTON, self.Reset)
                for i in range(0, 26):
                    self.buttons[i].Disable()
        self.pressed_buttons[strn] = True


ex = wx.App()
Hangman(None)
ex.MainLoop()