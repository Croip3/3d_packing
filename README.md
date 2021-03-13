# Relax Days Hackathon - 3D Packing

This project was created in the Relaxdays Code Challenge Vol. 1. See https://sites.google.com/relaxdays.de/hackathon-relaxdays/startseite for more information.

My participant ID in the challenge was: CC-VOL1-9, CC-Vol1-22

## How to run this project

Demo Video: https://youtu.be/4SQmrnVAc0A

You can get a running version of this code by using:

```bash
git clone https://github.com/Croip3/3d_packing.git
cd 3d_packing
docker build -t packing .
docker run -p 3000:3000 packing
```

How to use the algorithm

```bash
curl --request POST --data '{"packagecurl --request POST --data '{"package_types":[{"dimensions":[10,20,15],"cost":10},{"dimensions":[10,10,10],"cost":5}],"articles":[[10,10,5],[5,5,5],[9,4,5],[10,20,10],[10,10,10]]}' http://localhost:3000/

```
