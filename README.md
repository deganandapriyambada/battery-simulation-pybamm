Production

    gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app

Development

    uvicorn app:app --reload
