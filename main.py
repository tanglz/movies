from movie_meta_info import movie_mate_info, get_title_names
from screenplay import get_screenplays_from_simply_scripts, get_screenplays_from_daily_scripts, batch_download

if __name__ == '__main__':
    # get movie mate information
    # movie_mate_info()

    # # get screenplay
    # get movie titles
    # titles = get_title_names()
    # save screenplay semi-structured information from website:simply_scripts
    # filename = get_screenplays_from_simply_scripts(titles)

    # save screenplay semi-structured information from website:daily_scripts
    # filename = get_screenplays_from_daily_scripts(titles)

    # batch download screenplay
    result = batch_download("scripts_daily.json")

    if result:
        print("finished")
