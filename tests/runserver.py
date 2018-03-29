# coding: utf-8
import os
import subprocess
import server

server.simple_server(15000, daemon=False, dir=os.curdir)

