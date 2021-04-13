import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import pylab
import mqtt_client
import numpy

# Create figure for plotting
fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
fn = r'pic.jpeg'
im = plt.imread(fn)


# Initialize communication with TMP102
def on_click(event):
    mqtt_client.init()

def on_disconnect(event):
    mqtt_client.off_disconnect()

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Read temperature (Celsius) from TMP102
    # Add x and y to lists]
    circle1 = plt.Circle((0, 0), 2, color='r')
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    #xs.append(temp_c.date)
    custom_mess = mqtt_client.mess
    print(custom_mess)
    ys.append(custom_mess)
    if custom_mess > 1000:
        ax.set(facecolor='r')
    else:
        ax.set(facecolor='w')

    # Limit x and y lists to 20 items
    xs = xs[-50:]
    ys = ys[-50:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    ax.set(xlabel='time (s)', ylabel='CO2',
           title='CO2  over Time')

    # Format plot
    ax.tick_params(axis='x', labelrotation=45)
    #plt.xticks(rotation=55, ha='right')
    plt.subplots_adjust(bottom=0.30)

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)

axes_button_start = pylab.axes([0.2, 0.04, 0.15, 0.075])
axes_button_stop = pylab.axes([0.5, 0.04, 0.15, 0.075])
#indecator=pylab.axes([0.7, 0.04, 0.05, 0.075])

button_start = Button(axes_button_start, 'Start')
button_start.on_clicked(on_click)

button_stop = Button(axes_button_stop, 'Stop')
button_stop.on_clicked(on_disconnect)

plt.show()

