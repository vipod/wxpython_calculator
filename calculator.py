"""wxPython learning program: Integer Calculater

   Author: Vitaliy Podoba vitaliypodoba@gmail.com
"""

import wx

# list of math operations and digits to check against
OPERATIONS = ('/', '*', '-', '+')
DIGITS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

class Calculator(wx.Dialog):
    """Python Integer Calculator"""

    def __init__(self):
        # initialize our dialog window with: title and size
        wx.Dialog.__init__(self, None, id=-1, title='Calculator',
            size=wx.Size(182, 190))

        # sizers will allows us to put buttons into nice GRID layout
        sizer = wx.GridBagSizer(hgap=7, vgap=10)

        # add calculator display - text area in read-only mode
        # text inside will be right aligned
        self.display = wx.TextCtrl(self, id=-1, value='0',
            size=wx.Size(182, 40),
            style=wx.TE_READONLY|wx.TE_RIGHT)

        sizer.Add(self.display, (0, 0), (1, 4), wx.EXPAND)

        # put buttons into 4x4 grid
        x = 0
        y = 1
        for row in (('7', '8', '9', '/'),
                    ('4', '5', '6', '*'),
                    ('1', '2', '3', '-'),
                    ('0', 'C', '=', '+')):
            for blabel in row:
                # create button
                button = wx.Button(self, id=-1, label=blabel, size=wx.Size(40, 20))

                # bind mouse click on button
                self.Bind(wx.EVT_BUTTON, self.HandleButton, button)

                # add button to grid sizer
                sizer.Add(button, (y, x), (1, 1))
                x += 1

            x = 0
            y += 1

        # set a few variables for calculator to work
        self.operation = None   # remember last operation
        self.last = None        # remember last number entered
        self.resolved = None    # flag to clear screen after solve()

        # add our grid bag sizer to our dialog
        self.SetSizer(sizer)

        # set dialog centrally on the screen
        self.CenterOnScreen()

    def HandleButton(self, event):
        """This Calculator method is called on every button click"""
        # define event variables: button, it's label, text field value
        button = event.GetEventObject()
        label = button.GetLabel()
        value = self.getValue()

        # below we handle our event differently based on button clicked

        # Clear button
        if label == 'C':
            # simply reset display and forgot any custom calculator variables
            self.Clear()

        # digit button pressed
        elif label in DIGITS:
            # it's important to clear display before:
            # * new operation
            # * after zero digit
            # * and after solve() funtion, '=' button
            if value == '0' or value in OPERATIONS or self.resolved:
                self.update('')
                self.resolved = False

            self.display.AppendText(label)

        # equal sign: try to calculate results
        elif label == '=':
            # try to solve our equation
            self.solve()

        # clicked operation button
        elif label in OPERATIONS:
            # before any new operation try to solve previous operation
            self.solve()

            # remember previously entered number
            # if user is just changing operation - no need to remember any value
            if value not in OPERATIONS:
                self.last = self.getValue()

            # update last operation used and set display to operation label
            self.operation = label
            self.update(label)


    def Clear(self):
        """Calculator Clear button"""
        self.display.SetValue('0')
        self.operation = None
        self.last = None

    def update(self, value):
        """Shortcut for display update value"""
        self.display.SetValue(value)

    def getValue(self):
        """Shortcut for display get value"""
        return self.display.GetValue()

    def solve(self):
        """Equal operation: let's calculate result"""
        # only calculate anything if we got both: operation and last value
        if (self.last != None) and (self.operation != None):
            # here we use strings and eval to calculate result
            result =  str(eval(
                # e.g.  "67 - 24"
                self.last + self.operation + self.getValue()
            ))
            # finally reset calculator values and update display with result
            self.operation = None
            self.last = None
            self.update(result)
            self.resolved = True


def main():
    # run the application
    app = wx.App()

    # start calcualator dialog
    dlg = Calculator()
    dlg.ShowModal()
    dlg.Destroy()


# initialize our calculator
if __name__ == '__main__':
    main()
