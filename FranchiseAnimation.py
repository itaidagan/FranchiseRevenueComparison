from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

import operator

from animation_config import *

from collections import OrderedDict

import datetime
from datetime import date

import textwrap
import re

import DB_funcs

DONE = -1


class TextBox:
    def __init__(self, text_obj, birth_date):
        self.birth_date       = birth_date
        self.image_file = ''
        self.text_obj   = text_obj


class GraphLayout:
    def __init__(self):
        self.lines = []
        self.text_boxes = []


class FranchiseAnimation:
    def __init__(self):
        if READ_PARTIAL_DB:
            self.franchise_data_array       = DB_funcs.read_db(50)
        else:
            self.franchise_data_array       = DB_funcs.read_db()
        self.graph_layout               = 0
        self.franchise_date_ptr_array   = self.init_date_ptr_array()
        self.lines                      = []
        self.frame_dates                = self.create_date_array_for_animation()
        self.text_box_dict              = {}
        if HIGH_RES:
            self.dpi                        = 300
            self.figure                     = plt.figure(figsize=(W_HIGH_RES / self.dpi, H_HIGH_RES / self.dpi), dpi=self.dpi)
            self.fontsize                   = FONT_SIZE_H_RES
            self.height                     = H_HIGH_RES
            self.width                      = W_HIGH_RES
        else:
            self.dpi                        = 150
            self.figure                     = plt.figure(figsize=(W_LOW_RES / self.dpi, H_LOW_RES / self.dpi), dpi=self.dpi)
            self.fontsize                   = FONT_SIZE_L_RES
            self.height                     = H_LOW_RES
            self.width                      = W_LOW_RES
        self.ax                         = 0
        self.animation_end_delay_sec    = 15
        if ADD_END_DELAY:
            self.num_of_frames          = int(len(self.frame_dates) + 30*self.animation_end_delay_sec)
        else:
            self.num_of_frames          = int(len(self.frame_dates))
        self.earliest_date              = self.get_earliest_date()
        self.max_gross_to_date          = -1
        self.leaderboard            = {}
        self.franchise_tracker      = {}

    def create_date_array_for_animation(self):
        combined_dates = []
        for franchise_data in self.franchise_data_array:
            combined_dates = combined_dates + franchise_data.date_array
        unique_dates = list(OrderedDict.fromkeys(combined_dates))
        sorted_unique_dates = sorted(unique_dates)
        return sorted_unique_dates

    def get_earliest_date(self):
        earliest_date = datetime.datetime(year=2100, month=1, day=1)
        for franchise_data in self.franchise_data_array:
            if franchise_data.date_array[0] < earliest_date:
                earliest_date = franchise_data.date_array[0]
        return earliest_date

    def init_date_ptr_array(self):
        date_ptr_array = []
        for _ in self.franchise_data_array:
            date_ptr_array.append(0)
        return date_ptr_array

    def init_graph(self):
        plt.title("Franchise Earnings Comparison Over 20 Years", transform=None, x=self.width*0.10, y=self.height*0.90, ha='left')
        if TRACK_FRANCHISES:
            plt.subplots_adjust(left=0.1, right=0.75, top=0.8, bottom=0.1)
        else:
            plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)
        yformat = ticker.FormatStrFormatter("$%2.1fB")
        self.ax = plt.gca()
        self.ax.yaxis.set_major_formatter(yformat)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        for _ in self.franchise_data_array:
            line, = self.ax.step([], [], lw=1, where='post')
            self.lines.append(line)
        x_indent_2 = self.width*0.75
        y_indent_1 = self.height*0.88
        self.leaderboard['cur_date']    = self.ax.text(x_indent_2, y_indent_1, "", transform=None, fontsize=16, fontname='Monospace')
        self.ax.text(self.width*0.30, self.height*0.85, "(Adjusted for inflation)", transform=None, ha='left')

    def text_box_exists_for_film_name(self, film_name):
        if film_name in self.text_box_dict:
            return True
        return False

    def set_x_axis_locator(self, x_from, x_to):
        x_axis_range = x_to - x_from
        years = mdates.YearLocator()
        if x_axis_range < 200:
            self.ax.xaxis.set_major_locator(mdates.MonthLocator())
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
            # self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        elif x_axis_range < 7*365:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            self.ax.xaxis.set_major_locator(years)
            self.ax.xaxis.set_minor_locator(mdates.MonthLocator())
        else:
            self.ax.xaxis.set_major_locator(years)
            self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    def animate(self, i):
        # A sort of a progress bar
        if i > 0 and i % 100 == 0:
            print("Iteration %4s out of %s" % (i, self.num_of_frames))

        # No more frames to draw (but leave some delay for the static image or zoom-out)
        if i >= len(self.frame_dates):
            for text_box, value in self.text_box_dict.items():
                alpha = self.text_box_dict[text_box].text_obj.get_alpha()
                if alpha > 0.05:
                    alpha = alpha * 0.97
                    self.text_box_dict[text_box].text_obj.set_alpha(alpha)
                else:
                    self.text_box_dict[text_box].text_obj.set_text('')
            if ADD_ZOOM_OUT:
                [left, right] = self.ax.get_xlim()
                if left > date.toordinal(self.earliest_date):
                    left = left - 45
                    self.ax.set_xlim(left=left)
                    self.set_x_axis_locator(left, right)
            return self.lines

        cur_animation_day   = self.frame_dates[i]

        for n, franchise_data in enumerate(self.franchise_data_array):
            # Skip "completed" franchises
            if self.franchise_date_ptr_array[n] == DONE:
                continue

            # Update date pointer for each franchise, when two films are showing together you might need
            # to advance the pointer by two, hence the usage of a "while" loop
            while cur_animation_day > franchise_data.date_array[self.franchise_date_ptr_array[n]]:
                self.franchise_date_ptr_array[n] = self.franchise_date_ptr_array[n] + 1
                if self.franchise_date_ptr_array[n] == len(franchise_data.date_array):
                    self.franchise_date_ptr_array[n] = DONE

                    break

            cur_ptr = self.franchise_date_ptr_array[n]

            # Don't draw lines for dates that have yet to arrive
            if franchise_data.date_array[cur_ptr] > cur_animation_day or cur_ptr == 0:
                continue

            to_index = self.franchise_date_ptr_array[n]

            # Here is where we draw and redraw the updated graphs
            x = franchise_data.date_array[0:to_index]
            # y = franchise_data.gross_to_date_array[0:to_index]
            y = franchise_data.adjusted_gtd[0:to_index]
            max_y = max(y) if to_index > 0 else -1

            # This will be used for the Y axis limits
            if max_y > self.max_gross_to_date:
                self.max_gross_to_date = max_y

            self.lines[n].set_data(x, y)

            film_name = franchise_data.film_name_array[cur_ptr]

            if SHOW_FILM_NAMES:
                if not self.text_box_exists_for_film_name(film_name):  # New film and text box
                    film_name_wrapped = textwrap.wrap(franchise_data.film_name_array[cur_ptr], 14)
                    film_name_wrapped = "\n".join(film_name_wrapped)
                    new_text_obj = self.ax.text(x[-1], y[-1], film_name_wrapped, fontsize=self.fontsize, horizontalalignment='center', alpha=1)
                    new_text_box = TextBox(new_text_obj, franchise_data.date_array[cur_ptr])
                    self.text_box_dict[film_name] = new_text_box
                else:
                    if UPDATE_TEXT_BOX_LOC:
                        # Not a new film, just update the location of the text
                        self.text_box_dict[film_name].text_obj.set_position((x[-1], y[-1]*1.03))

                if EXPIRE_FILM_NAMES:
                    keys_to_del = []
                    for text_box, value in self.text_box_dict.items():
                        age = cur_animation_day - value.birth_date
                        if age > datetime.timedelta(days=365*3):
                            alpha = self.text_box_dict[text_box].text_obj.get_alpha()
                            if alpha > 0.05:
                                alpha = alpha * 0.97
                                self.text_box_dict[text_box].text_obj.set_alpha(alpha)
                            else:
                                self.text_box_dict[text_box].text_obj.set_text('')
                                keys_to_del.append(text_box)
                    for key in keys_to_del:
                        del self.text_box_dict[key]

        # Leaderboard calculations
        revenue_so_far_dict = {}
        for n, franchise_data in enumerate(self.franchise_data_array):
            if not self.franchise_date_ptr_array[n] == 0:
                revenue_so_far_dict[franchise_data.franchise_name] = franchise_data.adjusted_gtd[self.franchise_date_ptr_array[n]]
            else:
                revenue_so_far_dict[franchise_data.franchise_name] = 0
            sorted_revenues = sorted(revenue_so_far_dict.items(), key=operator.itemgetter(1))

        if SHOW_LEADERBOARD:
            cur_animation_day_str = cur_animation_day.strftime("%d-%m-%Y")
            self.leaderboard['cur_date'].set_text(cur_animation_day_str)

        # Update axes limits
        x_from = date.toordinal(self.frame_dates[0]) - 10
        x_to = max(date.toordinal(self.frame_dates[0]) + 100, date.toordinal(self.frame_dates[i]) + 40)

        if SLIDING_WINDOW:
            x_from = max(x_from, x_to - WINDOW_WIDTH*365)

        if TRACK_FRANCHISES:
            for franchise in sorted_revenues:
                franchise_name = franchise[0]
                franchise_revenue = franchise[1]
                if franchise_revenue > 0:
                    text_string = DB_funcs.make_franchise_name_succinct(franchise_name)
                    text_string = text_string + ("$%.2fbn" % franchise_revenue)
                    if franchise_name not in self.franchise_tracker:
                        franchise_text = self.ax.text(0, 0, text_string, ha='left', fontsize=6, fontname='Consolas')
                        franchise_text.set_x(x_to)
                        franchise_text.set_y(franchise_revenue)
                        self.franchise_tracker[franchise_name] = franchise_text
                    else:
                        self.franchise_tracker[franchise_name].set_x(x_to)
                        self.franchise_tracker[franchise_name].set_y(franchise_revenue)
                        self.franchise_tracker[franchise_name].set_text(text_string)

        self.ax.set_xlim(x_from, x_to)
        self.ax.set_ylim(0, max(self.max_gross_to_date * 1.3, 0.7))
        self.set_x_axis_locator(x_from, x_to)
        self.ax.figure.canvas.draw()
        return self.lines


my_animation    = FranchiseAnimation()
my_animation.init_graph()

animation       = animation.FuncAnimation(my_animation.figure,
                                          my_animation.animate,
                                          # init_func=my_animation.init_graph,
                                          frames=my_animation.num_of_frames,
                                          interval=30,
                                          blit=True)

file_name = str(datetime.datetime.now()) + '.mp4'
file_name = re.sub('[:]', '-', file_name)

plt.show()
# animation.save("Outputs//" + file_name, fps=30, extra_args=['-vcodec', 'libx264'])

