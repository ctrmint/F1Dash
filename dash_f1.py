#! /usr/bin/env python
# ---------------------------------------------------------------
# Codemasters F1 2016 UDP Telemetry Dashboard
# Revision  :   0.1
# Author    :   Mark Rodman
# ---------------------------------------------------------------

import os, sys, pygame, time, datetime
from dash_network import net_rx
from dash_network import receiver
from pygame.locals import *
from dash_support import *

class Rpm_ball(object):
    def __init__(self, name, revs, colour_int):
        self.name = name
        self.revs = revs
        self.colour_int = colour_int
        self.colour = BLACK
        self.start_x = 25
        self.start_y = 25
        self.x_inc = 50
        self.size = 20

    def draw_on(self):
        if self.colour_int == 1:
            sl_colour = GREEN
        elif self.colour_int == 2:
            sl_colour = SL_YELL_ON
        else:
            sl_colour = RED
        pygame.draw.circle(windowSurface, sl_colour, ((rpm_ball_start_x + (self.revs * self.x_inc)), rpm_ball_start_y),
                           self.size, 0)

    def draw_off(self):
        if self.colour_int == 1:
            sl_colour = SL_GREEN_OFF
        elif self.colour_int == 2:
            sl_colour = SL_YELL_OFF
        else:
            sl_colour = SL_RED_OFF
        pygame.draw.circle(windowSurface, sl_colour, ((rpm_ball_start_x + (self.revs * self.x_inc)), rpm_ball_start_y),
                           self.size, 0)

    def draw_blank(self):
        pygame.draw.circle(windowSurface, SL_OFF, ((rpm_ball_start_x + (self.revs * self.x_inc)), rpm_ball_start_y),
                           self.size, 0)

    def draw_max(self):
        pygame.draw.circle(windowSurface, SL_MAX, ((rpm_ball_start_x + (self.revs * self.x_inc)), rpm_ball_start_y),
                           self.size, 0)


class Basic_instrument_text(object):
    def __init__(self, name, text_string, fore_colour, back_colour, loc_x, loc_y):
        self.name = name
        self.text_string = text_string
        self.fore_colour = fore_colour
        self.back_colour = back_colour
        self.loc_x = loc_x
        self.loc_y = loc_y

    def draw_text(self):
        text = instruFont.render(self.text_string, True, self.fore_colour, self.back_colour)
        text_rect = text.get_rect()
        text_rect.centerx = 200
        text_rect.centery = 50
        # draw the text onto the surface
        windowSurface.blit(text, (self.loc_x, self.loc_y))


class Gear_indicator(object):
    def __init__(self, name, gear_state, fore_colour, back_colour):
        self.name = name
        self.gear_state = gear_state
        self.fore_colour = fore_colour
        self.back_colour = back_colour
        self.gear_conv_list = ['R', 'N', '1', '2', '3', '4', '5', '6', '7', '8']
        self.old_gear = self.gear_conv_list[self.gear_state]

    def draw_gear(self):
        # omitted back colour box
        text = basicFont.render(self.gear_conv_list[self.gear_state], True, self.fore_colour)
        text_rect = text.get_rect()
        text_rect.centerx = gear_x
        text_rect.centery = gear_y
        # draw the text onto the surface
        windowSurface.blit(text, text_rect)


    def update_gear(self, gear_state):
        # Draw rectangle onto screen to cover old gear
        pygame.draw.rect(windowSurface, BLACK, [348, 80, 122, 218])
        text = basicFont.render(self.gear_conv_list[gear_state], True, self.fore_colour)
        text_rect = text.get_rect()
        text_rect.centerx = gear_x
        text_rect.centery = gear_y
        # draw the text onto the surface
        windowSurface.blit(text, text_rect)


class Rpm_indicator(object):
    def __init__(self, name, rpm_float, rpm_forecolour, rpm_backcolour):
        self.name = name
        self.rpm_float = rpm_float
        self.rpm_forecolour = rpm_forecolour
        self.rpm_backcolour = rpm_backcolour

    def draw_rpm(self):
        current_rpm = int(self.rpm_float)
        rpm_text = rpmFont.render(str(current_rpm).center(8, ' '), True, self.rpm_forecolour, self.rpm_backcolour)
        rpm_rect = rpm_text.get_rect()
        rpm_rect.centerx = 65
        rpm_rect.centery = 105
        windowSurface.blit(rpm_text, rpm_rect)

    def update_rpm(self, rpm_float):
        self.rpm_float = rpm_float
        rpm_text = rpmFont.render(str(int(self.rpm_float)).center(8, ' '), True, self.rpm_forecolour, self.rpm_backcolour)
        rpm_rect = rpm_text.get_rect()
        rpm_rect.centerx = 65
        rpm_rect.centery = 105
        windowSurface.blit(rpm_text, rpm_rect)
        pygame.display.update()


class Mph_indicator(object):
    def __init__(self, name, mph_float, mph_forecolour, mph_backcolour):
        self.name = name
        self.mph_float = mph_float
        self.mph_forecolour = mph_forecolour
        self.mph_backcolour = mph_backcolour

    def draw_mph(self):
        current_mph = int(self.mph_float)
        mph_text = mphFont.render(str(current_mph).center(8, ' '), True, self.mph_forecolour, self.mph_backcolour)
        mph_rect = mph_text.get_rect()
        mph_rect.centerx = (display_width - 65)
        mph_rect.centery = 105
        windowSurface.blit(mph_text, mph_rect)

    def update_mph(self, mph_float):
        self.mph_float = mph_float
        mph_text = mphFont.render(str(int(self.mph_float)).center(8, ' '), True, self.mph_forecolour, self.mph_backcolour)
        mph_rect = mph_text.get_rect()
        mph_rect.centerx = (display_width - 65)
        mph_rect.centery = 105
        windowSurface.blit(mph_text, mph_rect)


class BrakeTemp_indicator(object):
    def __init__(self, name, temp_float, braketemp_forecolour, braketemp_backolour):
        self.name = name
        self.braketemp = temp_float
        self.braketemp_forecolour = braketemp_forecolour
        self.braketemp_backcolour = braketemp_backolour

    def draw_braketemp(self):
        if self.braketemp < 500:
            self.braketemp_forecolour = BLUE

        brake_text = brakeFont.render(str(int(self.braketemp)).center(8, ' '), True, self.braketemp_forecolour, self.braketemp_backcolour)
        brake_rect = brake_text.get_rect()
        brake_rect.centerx = (display_width - 65)
        brake_rect.centery = 200
        windowSurface.blit(brake_text, brake_rect)

    def update_braketemp(self, temp_float):
        self.braketemp = temp_float
        if self.braketemp < 500:
            self.braketemp_forecolour = BLUE
        brake_text = brakeFont.render(str(int(self.braketemp)).center(8, ' '), True, self.braketemp_forecolour, self.braketemp_backcolour)
        brake_rect = brake_text.get_rect()
        brake_rect.centerx = (display_width - 65)
        brake_rect.centery = 200
        windowSurface.blit(brake_text, brake_rect)


class PSI_indicator(object):
    def __init__(self, name, psi_float, psi_forecolour, psi_backolour):
        self.name = name
        self.psi_float = psi_float
        self.psi_forecolour = psi_forecolour
        self.psi_backcolour = psi_backolour

    def draw_psi(self):
        psi_text = brakeFont.render(str(int(self.psi_float)).center(8, ' '), True, self.psi_forecolour,
                                    self.psi_backcolour)
        psi_rect = psi_text.get_rect()
        psi_rect.centerx = 65
        psi_rect.centery = 200
        windowSurface.blit(psi_text, psi_rect)

    def update_psi(self, psi_float):
        self.psi_float = psi_float
        psi_text = brakeFont.render(str(int(self.psi_float)).center(8, ' '), True, self.psi_forecolour,
                                    self.psi_backcolour)
        psi_rect = psi_text.get_rect()
        psi_rect.centerx = 65
        psi_rect.centery = 200
        windowSurface.blit(psi_text, psi_rect)

class Last_Lap(object):
    def __init__(self, name, lastlap_float, lastlap_forecolour, lastlap_backcolour):
        self.name = name
        self.lastlap_float = lastlap_float
        self.laps = []
        self.laps_count = 0
        self.current_lastlap = 0
        self.past_lastlap = 0

    def update_lap(self, lastlap_float):
        self.current_lastlap = lastlap_float
        if self.current_lastlap == self.past_lastlap:
            print "..."
        else:
            self.laps.append(self.current_lastlap)
            self.laps_count += 1
            self.past_lastlap = self.current_lastlap
            print "Last lap updated :" + self.past_lastlap



# set up pygame
pygame.init()
pygame.font.init()


# find fonts  ----
available_fonts = pygame.font.get_fonts()
for font in range(len(available_fonts)):
    if available_fonts[font] == LCD_font:
        fontpath = pygame.font.match_font(available_fonts[font])

# set up fonts
basicFont = pygame.font.Font(fontpath, gear_fontsize)
instruFont = pygame.font.SysFont(None, instru_fontsize)
rpmFont = pygame.font.SysFont(None, rpm_fontsize)
mphFont = pygame.font.SysFont(None, rpm_fontsize)
brakeFont = pygame.font.SysFont(None, rpm_fontsize)

# set up the window
windowSurface = pygame.display.set_mode((display_width, display_height), 0, 32)
pygame.display.set_caption(display_title)

# draw the black background onto the surface
windowSurface.fill(BLACK)

def inital_setup():
    # draw screen formatting
    pygame.draw.line(windowSurface, TEXT_BG, (00, 50), (display_width, 50), display_line_width)
    pygame.draw.line(windowSurface, TEXT_BG, (00, 350), (display_width, 350), display_line_width)
    pygame.draw.line(windowSurface, TEXT_BG, (190, 50), (190, 350), display_line_width)
    pygame.draw.line(windowSurface, TEXT_BG, ((display_width - 190), 50), ((display_width - 190), 350),
                     display_line_width)
    rpm_key = Basic_instrument_text("rpm_key", "RPM", TEXT_INSTRU, BLACK, 128, 98)
    mph_key = Basic_instrument_text("mph_key", "MPH", TEXT_INSTRU, BLACK, (display_width - 157), 98)
    brake_key = Basic_instrument_text("Brake_key", "BRAKE", TEXT_INSTRU, BLACK, (display_width - 166), 195)
    psi_key = Basic_instrument_text("PSI_key", "PSI", TEXT_INSTRU, BLACK, 129, 195)
    rpm_key.draw_text()
    mph_key.draw_text()
    brake_key.draw_text()
    psi_key.draw_text()

    return


def initial_rpm():
    # Instantiate RPM ball objects
    global rpm_1k
    global rpm_2k
    global rpm_3k
    global rpm_4k
    global rpm_5k
    global rpm_6k
    global rpm_7k
    global rpm_8k
    global rpm_9k
    global rpm_10k
    global rpm_11k
    global rpm_12k
    global rpm_13k
    global rpm_14k
    global rpm_15k
    global rpm_16k
    rpm_1k = Rpm_ball("rpm_1k", 0, 1)
    rpm_2k = Rpm_ball("rpm_2k", 1, 1)
    rpm_3k = Rpm_ball("rpm_3k", 2, 1)
    rpm_4k = Rpm_ball("rpm_4k", 3, 1)
    rpm_5k = Rpm_ball("rpm_5k", 4, 1)
    rpm_6k = Rpm_ball("rpm_6k", 5, 1)
    rpm_7k = Rpm_ball("rpm_7k", 6, 1)
    rpm_8k = Rpm_ball("rpm_8k", 7, 1)
    rpm_9k = Rpm_ball("rpm_9k", 8, 1)
    rpm_10k = Rpm_ball("rpm_10k", 9, 1)
    rpm_11k = Rpm_ball("rpm_11k", 10, 2)
    rpm_12k = Rpm_ball("rpm_12k", 11, 2)
    rpm_13k = Rpm_ball("rpm_13k", 12, 2)
    rpm_14k = Rpm_ball("rpm_14k", 13, 3)
    rpm_15k = Rpm_ball("rpm_15k", 14, 3)
    rpm_16k = Rpm_ball("rpm_16k", 15, 3)
    return


def rpm_off():
    # Draw balls
    rpm_1k.draw_off()
    rpm_2k.draw_off()
    rpm_3k.draw_off()
    rpm_4k.draw_off()
    rpm_5k.draw_off()
    rpm_6k.draw_off()
    rpm_7k.draw_off()
    rpm_8k.draw_off()
    rpm_9k.draw_off()
    rpm_10k.draw_off()
    rpm_11k.draw_off()
    rpm_12k.draw_off()
    rpm_13k.draw_off()
    rpm_14k.draw_off()
    rpm_15k.draw_off()
    rpm_16k.draw_off()
    return


def rpm_blank():
    # Draw balls
    rpm_1k.draw_blank()
    rpm_2k.draw_blank()
    rpm_3k.draw_blank()
    rpm_4k.draw_blank()
    rpm_5k.draw_blank()
    rpm_6k.draw_blank()
    rpm_7k.draw_blank()
    rpm_8k.draw_blank()
    rpm_9k.draw_blank()
    rpm_10k.draw_blank()
    rpm_11k.draw_blank()
    rpm_12k.draw_blank()
    rpm_13k.draw_blank()
    rpm_14k.draw_blank()
    rpm_15k.draw_blank()
    rpm_16k.draw_blank()
    return


def rpm_on():
    # Draw balls
    rpm_1k.draw_on()
    rpm_2k.draw_on()
    rpm_3k.draw_on()
    rpm_4k.draw_on()
    rpm_5k.draw_on()
    rpm_6k.draw_on()
    rpm_7k.draw_on()
    rpm_8k.draw_on()
    rpm_9k.draw_on()
    rpm_10k.draw_on()
    rpm_11k.draw_on()
    rpm_12k.draw_on()
    rpm_13k.draw_on()
    rpm_14k.draw_on()
    rpm_15k.draw_on()
    rpm_16k.draw_on()
    return


def rpm_max():
    # Draw balls
    rpm_1k.draw_max()
    rpm_2k.draw_max()
    rpm_3k.draw_max()
    rpm_4k.draw_max()
    rpm_5k.draw_max()
    rpm_6k.draw_max()
    rpm_7k.draw_max()
    rpm_8k.draw_max()
    rpm_9k.draw_max()
    rpm_10k.draw_max()
    rpm_11k.draw_max()
    rpm_12k.draw_max()
    rpm_13k.draw_max()
    rpm_14k.draw_max()
    rpm_15k.draw_max()
    rpm_16k.draw_max()
    return


def calc_rpm(rpm_value):
    rpm_off()
    if rpm_value > rpm1:
        rpm_1k.draw_on()
    if rpm_value > rpm2:
        rpm_2k.draw_on()
    if rpm_value > rpm3:
        rpm_3k.draw_on()
    if rpm_value > rpm4:
        rpm_4k.draw_on()
    if rpm_value > rpm5:
        rpm_5k.draw_on()
    if rpm_value > rpm6:
        rpm_6k.draw_on()
    if rpm_value > rpm7:
        rpm_7k.draw_on()
    if rpm_value > rpm8:
        rpm_8k.draw_on()
    if rpm_value > rpm9:
        rpm_9k.draw_on()
    if rpm_value > rpm10:
        rpm_10k.draw_on()
    if rpm_value > rpm11:
        rpm_11k.draw_on()
    if rpm_value > rpm12:
        rpm_12k.draw_on()
    if rpm_value > rpm13:
        rpm_13k.draw_on()
    if rpm_value > rpm14:
        rpm_14k.draw_on()
    if rpm_value > rpm15:
        rpm_15k.draw_on()
    if rpm_value > rpm16:
        rpm_16k.draw_on()
    if rpm_value > rpm_max:
        rpm_max()
    return


def initiate_gear_display():
    global my_gear
    my_gear = Gear_indicator("mygear", 1, GREEN, BLACK)
    return


def initiate_rpm_text_display():
    global my_rpm
    my_rpm = Rpm_indicator("myrpm", 0.0, GREEN, TEXT_BG)
    return


def initiate_mph_text_display():
    global my_mph
    my_mph = Mph_indicator("mymph", 0.0, GREEN, TEXT_BG)
    return


def initiate_braketemp_text_display():
    global my_braketemp
    my_braketemp = BrakeTemp_indicator("mybreaktemp", 0.0, GREEN, TEXT_BG)
    return


def initiate_psi_text_display():
    global my_psi
    my_psi = PSI_indicator("mypsi", 0.0, GREEN, TEXT_BG)
    return


def pix_Array():
    # get a pixel array of the surface
    global pixArray
    pixArray = pygame.PixelArray(windowSurface)
    #pixArray[480][380] = BLACK
    pixArray[480][800] = BLACK
    del pixArray
    return


def rpm_process(current_rpm):
    if current_rpm > 12000.000:
        rpm_max()
    else:
        calc_rpm(int(current_rpm))
    return


def game_loop():
    rpm_value = 0
    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:                       # INTERACTIVE KEYBOARD DEBUG
                if event.key == K_UP:
                    rpm_on()
                if event.key == K_DOWN:
                    rpm_off()
                if event.key == K_LEFT:
                    rpm_max()
                if event.key == K_1:
                    my_gear.update_gear(1)
                if event.key == K_2:
                    my_gear.update_gear(2)
                if event.key == K_3:
                    my_gear.update_gear(3)
                if event.key == K_4:
                    my_gear.update_gear(4)
                if event.key == K_5:
                    my_gear.update_gear(5)
                if event.key == K_6:
                    my_gear.update_gear(6)
                if event.key == K_7:
                    my_gear.update_gear(7)
                if event.key == K_8:
                    my_gear.update_gear(8)
                if event.key == K_9:
                    my_gear.update_gear(9)
                if event.key == K_0:
                    my_gear.update_gear(0)
                if event.key == K_r:
                    rpm_value = 0
                    rpm_off()
                if event.key == K_q:
                    rpm_value += 1000
                    if rpm_value > 12000:
                        rpm_max()
                    else:
                        calc_rpm(rpm_value)
                if event.key == K_a:
                    rpm_value -= 1000
                    if rpm_value > 12000:
                        rpm_on()
                    else:
                        calc_rpm(rpm_value)
            elif event.type == USEREVENT:
                    rpm_off()

        data_gear, data_mph_fix, data_brake, data_rpm, data_psi, data_sector, data_sector1, data_sector2, data_lastlap, data_fuel_in_tank, data_fuel_capacity = receiver()

        my_gear.update_gear(int(data_gear))
        my_rpm.update_rpm(data_rpm)
        my_mph.update_mph(data_mph_fix)
        my_braketemp.update_braketemp(data_brake)
        my_psi.update_psi(data_psi)
        rpm_process(data_rpm)


        pygame.display.update()
    return


def main():
    inital_setup()
    pix_Array()
    initial_rpm()
    rpm_blank()
    initiate_gear_display()
    initiate_rpm_text_display()
    initiate_mph_text_display()
    initiate_braketemp_text_display()
    initiate_psi_text_display()
    my_gear.draw_gear()
    my_rpm.draw_rpm()
    my_mph.draw_mph()
    my_braketemp.draw_braketemp()
    my_psi.draw_psi()
    pygame.display.update()                                     # REFRESH THE DISPLAY
    game_loop()
    return


if __name__ == '__main__':

    main()
