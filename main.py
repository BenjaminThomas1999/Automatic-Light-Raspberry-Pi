{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPO1zLcQJobvVKuOBWNX1oI",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/BenjaminThomas1999/Automatic-Light-Raspberry-Pi/blob/master/main.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 232
        },
        "id": "UKH3ee5boJF-",
        "outputId": "16456048-c5ba-44fc-9140-446fffeaae0e"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "FileNotFoundError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mFileNotFoundError\u001b[0m                         Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-ebff228a988f>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     68\u001b[0m     \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"    1   2   3   4   5   6   7   8   9   10  11  12\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     69\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 70\u001b[0;31m Drones = [Drone(open(\"Route001.txt\", \"r\").read().split(\"\\n\"), \"Drone 1\"),\n\u001b[0m\u001b[1;32m     71\u001b[0m           \u001b[0mDrone\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Route002.txt\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m\"r\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msplit\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"\\n\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m\"Drone 2\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     72\u001b[0m           Drone(open(\"Route003.txt\", \"r\").read().split(\"\\n\"), \"Drone 3\")]\n",
            "\u001b[0;31mFileNotFoundError\u001b[0m: [Errno 2] No such file or directory: 'Route001.txt'"
          ]
        }
      ],
      "source": [
        "class Drone:\n",
        "  def __init__(self, data, name):\n",
        "    self.directions = data[2:]\n",
        "    self.directions.remove(\"\")\n",
        "    self.x = int(data[0])-1\n",
        "    self.y = int(data[1])-1\n",
        "    self.name = name\n",
        "    self.map = []\n",
        "    for y in range(12):\n",
        "      self.map.append([])\n",
        "      for x in range(12):\n",
        "        self.map[y].append('    ')\n",
        "    \n",
        "    self.errorMessage = \"\"\n",
        "\n",
        "\n",
        "    self.writeToMap(self.x, self.y, icon=\"S\")\n",
        "  \n",
        "  def predictRoute(self):\n",
        "    for count, direction in enumerate(self.directions):\n",
        "      if direction == \"N\":\n",
        "        self.y += 1\n",
        "        icon = '↑'\n",
        "      elif direction == \"S\":\n",
        "        self.y -= 1\n",
        "        icon = '↓'\n",
        "      elif direction == \"W\":\n",
        "        self.x -= 1\n",
        "        icon = \"←\"\n",
        "      elif direction == \"E\":\n",
        "        self.x += 1\n",
        "        icon = \"→\"\n",
        "\n",
        "      if(count < len(self.directions) -1):\n",
        "        if self.directions[count+1] == \"N\":\n",
        "          icon = '↑'\n",
        "        elif self.directions[count+1] == \"S\":\n",
        "          icon = '↓'\n",
        "        elif self.directions[count+1] == \"W\":\n",
        "          icon = \"←\"\n",
        "        elif self.directions[count+1] == \"E\":\n",
        "          icon = \"→\"\n",
        "      else:\n",
        "        icon = \"X\"\n",
        "\n",
        "      if(0 <= self.x <= 12 and 0 <= self.y <= 12):\n",
        "        self.writeToMap(self.x, self.y, icon = icon)\n",
        "      else:\n",
        "        self.errorMessage = \"Error: Predicted route takes the drone off the grid!\"\n",
        "        return -1\n",
        "\n",
        "\n",
        "\n",
        "  def writeToMap(self, x, y, icon=\"x\"):\n",
        "    self.map[x][y] = \" \" + icon + \"  \"\n",
        "\n",
        "  def printMap(self):\n",
        "    print(\"\\n------------------- \" + self.name + \" ----------------------\")\n",
        "    print(self.errorMessage)\n",
        "    for y in range(11, -1, -1):\n",
        "      space = \"  \"\n",
        "      if y > 8:\n",
        "        space = \" \"\n",
        "      print(y+1, end = space)\n",
        "      for x in range(12):\n",
        "        print(self.map[x][y], end=\"\")\n",
        "      print(\"\\n\")\n",
        "    print(\"    1   2   3   4   5   6   7   8   9   10  11  12\")\n",
        "\n",
        "Drones = [Drone(open(\"Route001.txt\", \"r\").read().split(\"\\n\"), \"Drone 1\"),\n",
        "          Drone(open(\"Route002.txt\", \"r\").read().split(\"\\n\"), \"Drone 2\"),\n",
        "          Drone(open(\"Route003.txt\", \"r\").read().split(\"\\n\"), \"Drone 3\")]\n",
        "\n",
        "print(\"S marks the start of the route, X marks the end.\", end=\"\\n\\n\")\n",
        "\n",
        "for drone in Drones:\n",
        "  drone.predictRoute()\n",
        "  drone.printMap()\n",
        "\n",
        "while True:\n",
        "  filename = input(\"Enter filename of further route file: \")\n",
        "  if filename == \"STOP\":\n",
        "    break\n",
        "  drone = Drone(open(filename, \"r\").read().split(\"\\n\"), filename)\n",
        "  drone.predictRoute()\n",
        "  drone.printMap()"
      ]
    }
  ]
}