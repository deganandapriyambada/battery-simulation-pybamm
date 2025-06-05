Dataset Sources:

1.Battery SOC

    Kollmeyer, Philip; Vidal, Carlos; Naguib, Mina; Skells, Michael (2020), “LG 18650HG2 Li-ion Battery Data and Example Deep Neural Network xEV SOC Estimator Script”, Mendeley Data, V3, doi: 10.17632/cp3473x7xv.3

Production

    gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

Development - Run on the root of /battery-ml-api folder

    uvicorn app.main:app --reload
