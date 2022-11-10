import unittest
import tkinter as tk
from frames.DifficultyFrame import DifficultyFrame
from frames.CharacterFrame import CharacterFrame

class UITesting(unittest.TestCase):
    t = tk.Tk()
    cf = CharacterFrame(t)
    df = DifficultyFrame(t)

    def testAddBtn(self):
        for i in range(8):
            self.cf.addCharacterBtn.invoke()
            assert len(self.cf.characters) <= i+2

    def testRemoveBtn(self):
        for i in range(8):
            self.cf.removeCharacterBtn.invoke()
            assert len(self.cf.characters) <= 8 - i - 1 or len(self.cf.characters) == 1

    def testLvlSpinbox(self):
        # move through every character row, and test all levels are accurate
        lvls = range(1,21)
        chars = self.cf.characters
        for i in range(8):
            assert int(chars[i]['level'].get()) == int(lvls[0])
            for j in range(1,20):
                chars[i]['level'].invoke('buttonup')
                assert int(chars[i]['level'].get()) == int(lvls[j])

            self.cf.addCharacterBtn.invoke()

        #now decrement buttons
        for i in range(8):
            for j in range(0,20):
                assert int(chars[8-i-1]['level'].get()) == int(lvls[20 - j-1])
                chars[8-i-1]['level'].invoke('buttondown')
            assert int(chars[8-i-1]['level'].get()) == int(lvls[0])
            self.cf.removeCharacterBtn.invoke()

    # def testMonsterSearch(mw, cf, df):
    #     # get 4 characters
    #     # set difficulty to medium
    #     #similuate elastic search
    #     pass

    def testDifficultyRadio(self):
        difficulties = ['Easy', 'Medium', 'Hard', 'Deadly']

        #print(df.diff.get())
        assert int(self.df.diff.get()) == difficulties.index('Easy')

        #change to medium
        self.df.R2.invoke()
        assert int(self.df.diff.get()) == difficulties.index('Medium')

        #change to hard
        self.df.R3.invoke()
        assert int(self.df.diff.get()) == difficulties.index('Hard')

        #change to deadly
        self.df.R4.invoke()
        assert int(self.df.diff.get()) == difficulties.index('Deadly')

        #change back to easy
        self.df.R1.invoke()
        assert int(self.df.diff.get()) == difficulties.index('Easy')

if __name__ == "__main__":
    unittest.main()
