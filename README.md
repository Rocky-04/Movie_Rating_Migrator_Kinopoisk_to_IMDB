# Movie Rating Migrator: Kinopoisk → IMDB

> **⚠️ PROJECT IS NO LONGER MAINTAINED**
>
> This project is archived and no longer actively maintained. The code is provided as-is for reference purposes only.

## About

A tool for downloading personal ratings from Kinopoisk in Excel format and migrating ratings from Kinopoisk to IMDB.

<p align="center">
  <img src="https://i.ibb.co/R9XL3F3/Screenshot-41.png" alt="Screenshot-41">
</p>

## Download Pre-built Application

**You can download a ready-to-use version of the application from this branch:**

🔗 **Branch with .rar file:** [`claude/revert-to-commit-6c9744f-011CUq1LS6nREcVrt8Cy8Eg8`](https://github.com/Rocky-04/Movie_Rating_Migrator_Kinopoisk_to_IMDB/tree/claude/revert-to-commit-6c9744f-011CUq1LS6nREcVrt8Cy8Eg8)

📦 **Direct download:** [`__Movie_Rating_Migrator_Kinopoisk_to_IMDB.rar`](https://github.com/Rocky-04/Movie_Rating_Migrator_Kinopoisk_to_IMDB/raw/claude/revert-to-commit-6c9744f-011CUq1LS6nREcVrt8Cy8Eg8/__Movie_Rating_Migrator_Kinopoisk_to_IMDB.rar)

## Requirements

1. Google Chrome browser
2. Access to Kinopoisk website (VPN may be required in some regions)
3. The application was developed for Windows (not tested on other operating systems)

## How to Use (Pre-built Version)

1. Download the file `__Movie_Rating_Migrator_Kinopoisk_to_IMDB.rar` from the link above and extract it
2. Run `__Movie_Rating_Migrator_Kinopoisk_to_IMDB.exe`
3. Enter the Kinopoisk user ID whose ratings you want to parse, and specify the path to save files
4. Follow the program instructions

## FAQ

### How to find Kinopoisk user ID?

You can find the ID in the ratings tab.


<p align="center">
  <img src="https://i.postimg.cc/ZKtTRCqV/Screenshot-1.png" alt="Screenshot-41">
</p>

### What if the browser doesn't open?

Most often this is due to driver version mismatch. Try updating the browser drivers:
1. Download the latest chromedriver version for your system [here](https://chromedriver.chromium.org/downloads)
2. Replace chromedriver.exe in the chrome_driver folder with your download

Make sure Kinopoisk website opens in your browser. In Ukraine it's blocked - any VPN will help fix this.

### What format will I receive ratings in after parsing?

You will receive ratings in Excel format. The file will contain the following columns:

- russian_movie_name
- english_movie_name
- user_rating
- week
- user_rating_count
- kinopoisk_id
- kinopoisk_rating
- imdb_id

A JSON format file will also be generated for further transfer of ratings to IMDB.

### Will all ratings be transferred to IMDB?

All ratings for which there is an IMDB code will be transferred. If a movie is not transferred, it will be added to an error file (created at the end of the rating transfer).

### What if the rating transfer fails?

The program remembers its working status. Launch the rating transfer again and it will continue from where it left off (it will also try to transfer movies that failed to transfer again).

Do not restart rating parsing, as the process will start from the beginning.

### How many movies are usually transferred successfully?

From practice, 99%. The rest end up in the error file.

## License

This project includes a LICENSE file. Please refer to it for usage terms.
