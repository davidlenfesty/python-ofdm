# Python-OFDM

## Introduction

This is a small program/simulation/whatever meant to emulate an OFDM modem.
This is the pilot work for creating an underwater communications system for ARVP.
Eventually I want to put this on an FPGA. (will it fit on an iCE40 I wonder?)

Lot's of credit to [dspillustrations.com](https://dspillustrations.com/pages/posts/misc/python-ofdm-example.html),
the linked post has been super useful to me, and while I try to claim I came up with most of this code
myself, it would have taken a LOT longer to do without this post.

## OFDM Background ##

### TODO

I should write stuff down here to help solidify my mental model of OFDM, but for now, you get nothing.

## Future plans

I want this to actually do something at some point, so I want to implement more.

For example, I need to implement something that mimics how a receiver would actually work, where it is unsure of where the packet starts.
As well, I want to implement some sort of communications protocol. And figure out how we could easily integrate it with
software on the robot.
