# SSSB-notifier

Small Python script to scrape the Stockholm student housing queue SSSB, assisting with checking when new apartments have arrived and then smoothly notifiying you via email.



## Installation

### Dependencies

The Selenium web driver has been used in order to scrape the SSSB webpage. This is the only non-Python dependency. Install it with the following command:

```shell
pip install -r requirements.txt
```

### Email

In order to send an email to you once new apartments arrive an email server is required. This is implemented via three environment variables that you have to set, assuming `smtp.gmail.com` server is used:

```shell
export GMAIL_USER = "sender-email@gmail.com"
export GMAIL_PASSWORD = "sender-password"
export RECEIVING_USER = "receiver@email.com"
```

If you wish to use another SMTP-server of your choice you can change the `server` variable in the `sendMail(..)` function.

### Update frequency

Once launched, the script will fetch data from SSSB every hour. This frequency can easily be changed by altering the parameter `updateFrequencyInSeconds`, placed in `main()`.



## Comment on functionality

Observe that the trigger is based on the number of available apartments changing, and will thus include SSSB lowering the amount of available apartments as well - i.e. there will be a few false positives. However, most of the time SSSB releases a batch with new ones which will be captured correctly. We can not simply check if the new number is greater than the previous either, since our update frequency is not capturing every single apartment added/removed. This script will thus capture most events correctly and definitely be an assisting hand when searching for apartments via SSSB.



## License

This project is licensed under the GNU License - see the [LICENSE.md](./LICENSE.md) file for details.