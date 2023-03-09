from main import *


def run():
    obs = OBS()
    obs._obs_client = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
    obs._obs_client.connect()

    # obs.prepare_team(Sides.RADIANT, PhotosKupleve)
    # obs.prepare_team(Sides.DIRE, PhotosPlintusa)

    obs.prepare_team(Sides.DIRE, PhotosBMSHB)
    obs.prepare_team(Sides.RADIANT, PhotosRejects)


if __name__ == '__main__':
    run()
