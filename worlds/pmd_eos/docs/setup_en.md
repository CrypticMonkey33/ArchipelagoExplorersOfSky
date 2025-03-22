# Setup Guide for Pokémon Mystery Dungeon: Explorers of Sky

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.
The EoS APWorld is still in development, so expect bugs! If you find a bug that hasn't already been reported, please open an issue on the GitHub issues page!

## Required Software

- BizHawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.9.1 is recommended; 2.10 is currently unable to connect.
  - Detailed installation instructions for BizHawk can be found at the above link.
  - Windows users must run the prerequisite installer first, which can also be found at the above link.
- The built-in BizHawk client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
- A .nds file for the EU version of Pokémon Mystery Dungeon: Explorers of Sky

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

Install the download .apworld file with the Archipelago Launcher. In the launcher, click "Generate Template Options" to generate a template YAML for EoS. You can make a copy of this template, and edit it to configure your settings.

## Joining a MultiWorld Game

### Obtain your NDS patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apeos` extension. 

Double-click on your `.apeos` file to start your client and start the ROM patch process. Once the process is finished, the client and the emulator will be started automatically, if you associated the extension to the client as recommended. If the extension isn't associated', select the BizHawk client or the Archipelago Launcher as the program to open the `.apeos` file with.

### Connect client to emulator

Once both the client and the emulator are started, you must connect them, if this is not done automatically. Within the emulator click on the "Tools" menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua script.

Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.

### Connect to the Multiserver

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

