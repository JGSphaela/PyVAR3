import matplotlib.pyplot as plt
import matplotlib.animation as animation
from temp_test import temp_test  # Your function that returns the temperature as a string

def get_temperature():
    """
    Calls temp_test(), converts the returned string to a float, and returns it.
    Adjust error handling if the string format is different.
    """
    try:
        return float(temp_test())
    except ValueError:
        # If conversion fails, you might want to return a default value or skip the update
        return None

# Create a figure and axis
fig, ax = plt.subplots()
x_vals = []  # To hold the time (in seconds)
y_vals = []  # To hold the temperature values

# Create a line that we will update during the animation.
(line,) = ax.plot([], [], 'r-', lw=2)

# Set up the plot labels and title
ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature")
ax.set_title("Real-Time Temperature Plot")

def init():
    """Initialize the background of the plot."""
    ax.set_xlim(0, 60)  # start with 60 seconds; this will auto-update later if needed
    ax.set_ylim(0, 100)  # set a reasonable temperature range; adjust as needed
    line.set_data(x_vals, y_vals)
    return line,

def update(frame):
    """
    This function is called every second (or every interval).
    'frame' is the current frame count.
    """
    # Get the current temperature reading
    current_temp = get_temperature()
    if current_temp is not None:
        x_vals.append(frame)        # Use the frame count as the time (assuming 1 frame = 1 second)
        y_vals.append(current_temp) # Append the current temperature

    # Optionally, adjust the x-axis limits if necessary:
    if frame > ax.get_xlim()[1]:
        ax.set_xlim(0, frame + 10)

    line.set_data(x_vals, y_vals)
    return line,

# Create the animation: interval is set in milliseconds (1000 ms = 1 second)
ani = animation.FuncAnimation(fig, update, init_func=init, interval=1000, blit=True)

# Display the plot
plt.show()
