*** Settings ***
Documentation   This script starts two teleporters and makes a call
Library         Remote    http://${ADDRESS_ALPHA}:${PORT}       WITH NAME       R_ALPHA
Library         Remote    http://${ADDRESS_OMEGA}:${PORT}       WITH NAME       R_OMEGA


*** Variables ***
${ADDRESS_ALPHA}   pi104
${ADDRESS_OMEGA}   pi108
${PORT}            8270

*** Test Cases ***
Make a call with a happy path
     R_ALPHA.Testus      Alpha  This is Alpha
     R_OMEGA.Testus      Omega  This is Omega
