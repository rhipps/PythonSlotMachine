# PythonSlotMachine
Initial attempt at creating a small slot machine UI written in Python using Tkinter. The app can be run in x-window mode on a raspberry pi as a small kiosk computer.

### slotmachineconfig
3 field config file 

1. The image theme directory to be read from `themes`
2. True / False if you want to start in full screen mode
3. Configurable jackpot value

### Creating a new theme
A theme is just a fancy name for the 4 images used on the slot rails when the slotmachine is running. 

To create a new theme just create a folder in the `themes` directory with your themes name and then create 4 `.png` images named `slotImg1.png` `slotImg2.png` `slotImg3.png`, and `slotImg4.png`.