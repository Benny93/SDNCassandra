#!/usr/bin/env bash
PATH_RYU_APP='~/sf_SDN/ryu/ryu/app/'
OPTIONS=' --verbose --observe-links '
APP_NAME='simple_switch_13.py'
APP2_NAME='ws_topology.py'
ryu-manager ${OPTIONS} "ryu.app.ws_topology"