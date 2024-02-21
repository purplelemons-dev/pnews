from init import main

while True:
    try:
        main()
    except Exception as e:
        print(e)
        main()
