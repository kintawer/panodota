from aiohttp import web
from obswebsocket import obsws, requests, events

OBS_HOST = "localhost"
OBS_PORT = 4444
OBS_PASSWORD = "secret"
SOLO_URL_TEMPLATE = 'https://vdo.ninja/?view={}&solo&room=panodota&password=123&sl&q&appbg={}'
TEAM_SCENE_1_URL = 'https://vdo.ninja/?scene=1&room=panodota&password=123&916'
TEAM_SCENE_2_URL = 'https://vdo.ninja/?scene=2&room=panodota&password=123&916'


class Sides:
    DIRE = 'dire'
    RADIANT = 'radiant'


class GameStates:
    DOTA_GAMERULES_STATE_INIT = "DOTA_GAMERULES_STATE_INIT"
    DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD = "DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD"
    DOTA_GAMERULES_STATE_HERO_SELECTION = "DOTA_GAMERULES_STATE_HERO_SELECTION"
    DOTA_GAMERULES_STATE_STRATEGY_TIME = "DOTA_GAMERULES_STATE_STRATEGY_TIME"
    DOTA_GAMERULES_STATE_PRE_GAME = "DOTA_GAMERULES_STATE_PRE_GAME"
    DOTA_GAMERULES_STATE_GAME_IN_PROGRESS = "DOTA_GAMERULES_STATE_GAME_IN_PROGRESS"
    DOTA_GAMERULES_STATE_POST_GAME = "DOTA_GAMERULES_STATE_POST_GAME"
    DOTA_GAMERULES_STATE_DISCONNECT = "DOTA_GAMERULES_STATE_DISCONNECT"
    DOTA_GAMERULES_STATE_TEAM_SHOWCASE = "DOTA_GAMERULES_STATE_TEAM_SHOWCASE"
    DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP = "DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP"
    DOTA_GAMERULES_STATE_WAIT_FOR_MAP_TO_LOAD = "DOTA_GAMERULES_STATE_WAIT_FOR_MAP_TO_LOAD"
    DOTA_GAMERULES_STATE_LAST = "DOTA_GAMERULES_STATE_LAST"


class Scenes:
    IDLE = 'panodota_idle'
    PICKS = 'panodota_picks'
    CLEAN_GAME = 'panodota_clean_game'
    GAME = 'panodota_game'


class Cameras:
    TEAM_1 = 'team_1'
    TEAM_2 = 'team_2'

    PLAYER_0 = 'camera_player0'
    PLAYER_1 = 'camera_player1'
    PLAYER_2 = 'camera_player2'
    PLAYER_3 = 'camera_player3'
    PLAYER_4 = 'camera_player4'
    PLAYER_5 = 'camera_player5'
    PLAYER_6 = 'camera_player6'
    PLAYER_7 = 'camera_player7'
    PLAYER_8 = 'camera_player8'
    PLAYER_9 = 'camera_player9'

    RADIANT = (PLAYER_0, PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4)
    DIRE = (PLAYER_5, PLAYER_6, PLAYER_7, PLAYER_8, PLAYER_9)
    PLAYERS = (
        PLAYER_0, PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4,
        PLAYER_5, PLAYER_6, PLAYER_7, PLAYER_8, PLAYER_9,
    )

    @staticmethod
    def get_camera_id_by_gsi(gsi_player_id):
        return f'camera_{gsi_player_id}'


class Photos:
    TEAM = ''

    POS_1_NAME = ''
    POS_2_NAME = ''
    POS_3_NAME = ''
    POS_4_NAME = ''
    POS_5_NAME = ''
    POS_1 = ''
    POS_2 = ''
    POS_3 = ''
    POS_4 = ''
    POS_5 = ''

    TEAM_SCENE_URL = ''
    ALL = (
        (POS_1_NAME, POS_1),
        (POS_2_NAME, POS_2),
        (POS_3_NAME, POS_3),
        (POS_4_NAME, POS_4),
        (POS_5_NAME, POS_5),
    )


class PhotosKupleve(Photos):
    TEAM = 'Kupleve'

    POS_1_NAME = 'Федос'
    POS_2_NAME = 'Ребрик'
    POS_3_NAME = 'Хус'
    POS_4_NAME = 'Крысанов'
    POS_5_NAME = 'Михайлов'
    POS_1 = 'https://ca.slack-edge.com/TEK27331D-U02P7H035Q9-06c2ac9615ba-512'  # fedos
    POS_2 = 'https://ca.slack-edge.com/TEK27331D-U014LKSC9T4-ffcca9b60a05-512'  # rebrik
    POS_3 = 'https://ca.slack-edge.com/TEK27331D-U013KL2NJFQ-4d9aebe530be-512'  # hus
    POS_4 = 'https://ca.slack-edge.com/TEK27331D-U02N1JK8W2K-01eb61ac17d1-512'  # krisanov
    POS_5 = 'https://ca.slack-edge.com/TEK27331D-U02ND9SNRPW-11dff9b3fc5f-512'  # mikhailov
    # 1 fedos, 2 rebrik, 3 hus, 4 krisanov, 5 mikhailov

    TEAM_SCENE_URL = TEAM_SCENE_1_URL
    ALL = (
        (POS_1_NAME, POS_1),
        (POS_2_NAME, POS_2),
        (POS_3_NAME, POS_3),
        (POS_4_NAME, POS_4),
        (POS_5_NAME, POS_5),
    )


class PhotosPlintusa(Photos):
    TEAM = 'Plintus'

    POS_1_NAME = 'Тигран'
    POS_2_NAME = 'Чинчик'
    POS_3_NAME = 'Петя'
    POS_4_NAME = 'Влад'
    POS_5_NAME = 'Таня'
    POS_1 = 'https://ca.slack-edge.com/TEK27331D-U02FWJQ3L80-488e0eacbf75-512'
    POS_2 = 'https://ca.slack-edge.com/TEK27331D-U02MG2V3PD2-d418eeb24b0d-512'
    POS_3 = 'https://ca.slack-edge.com/TEK27331D-U02JXAD4L94-8bcb866df742-512'
    POS_4 = 'https://ca.slack-edge.com/TEK27331D-U02MRTY86BT-4133bc582e3b-512'
    POS_5 = 'https://ca.slack-edge.com/TEK27331D-U012GNPP8NN-13de2b9cf529-512'

    TEAM_SCENE_URL = TEAM_SCENE_2_URL
    ALL = (
        (POS_1_NAME, POS_1),
        (POS_2_NAME, POS_2),
        (POS_3_NAME, POS_3),
        (POS_4_NAME, POS_4),
        (POS_5_NAME, POS_5),
    )


class PhotosRejects(Photos):
    TEAM = 'pano.rejects'

    POS_1_NAME = 'Дима Щетинский'
    POS_2_NAME = 'Саня Мащак'
    POS_3_NAME = 'Никита Куракин'
    POS_4_NAME = 'Кирилл Тимонин'
    POS_5_NAME = 'Андрей Елисафенко'

    POS_1 = 'https://ca.slack-edge.com/TEK27331D-U02FD9AN7B6-2b3242355cc6-512'
    POS_2 = 'https://ca.slack-edge.com/TEK27331D-U02FWMN5MJ4-47b6d31c7f76-512'
    POS_3 = 'https://ca.slack-edge.com/TEK27331D-U03JY43PFN2-a007f6cde4f5-512'
    POS_4 = 'https://ca.slack-edge.com/TEK27331D-U0153TC0R8V-98ca48be0c03-512'
    POS_5 = 'https://ca.slack-edge.com/TEK27331D-U02FWMWVCKA-e8f7998b10c5-512'

    TEAM_SCENE_URL = TEAM_SCENE_2_URL
    ALL = (
        (POS_1_NAME, POS_1),
        (POS_2_NAME, POS_2),
        (POS_3_NAME, POS_3),
        (POS_4_NAME, POS_4),
        (POS_5_NAME, POS_5),
    )


class PhotosBMSHB(Photos):
    TEAM = 'BMSHB'

    POS_1_NAME = 'Саша Шустров'
    POS_2_NAME = 'Никита Кудряшов'
    POS_3_NAME = 'Михасл Бритиков'
    POS_4_NAME = 'Костя Лукьянчиков'
    POS_5_NAME = 'Саша Тимофеев'

    POS_1 = 'https://ca.slack-edge.com/TEK27331D-UNA0N116V-482882800d92-512'
    POS_2 = 'https://ca.slack-edge.com/TEK27331D-U015BRJDY2V-ca8c3096b2d7-512'
    POS_3 = 'https://ca.slack-edge.com/TEK27331D-U014FA72BPH-12b674220e0e-512'
    POS_4 = 'https://ca.slack-edge.com/TEK27331D-U02FWJNBCRW-efe7e8700169-512'
    POS_5 = 'https://ca.slack-edge.com/TEK27331D-U013DTVKBB6-36cbe3ea3862-512'

    TEAM_SCENE_URL = TEAM_SCENE_1_URL
    ALL = (
        (POS_1_NAME, POS_1),
        (POS_2_NAME, POS_2),
        (POS_3_NAME, POS_3),
        (POS_4_NAME, POS_4),
        (POS_5_NAME, POS_5),
    )


class OBS:
    def __init__(self):
        self._obs_client: obsws = None

        self.current_scene = None
        self.camera_state = {}
        self.callbacks = {}

    def init(self):
        self._obs_client = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        self._obs_client.connect()
        self._obs_client.register(self.update_current_scene, events.SwitchScenes)

        self.update_current_scene()
        self.update_camera_state()

        self.callbacks = {
            None: self._callback_idle,
            GameStates.DOTA_GAMERULES_STATE_HERO_SELECTION: self._callback_picks,
            GameStates.DOTA_GAMERULES_STATE_TEAM_SHOWCASE: self._callback_clean_game,
            GameStates.DOTA_GAMERULES_STATE_PRE_GAME: self._callback_game,
            GameStates.DOTA_GAMERULES_STATE_GAME_IN_PROGRESS: self._callback_game,
        }
        print(f'OBS: current_scene = {self.current_scene}, camera_state = {self.camera_state}')

    def shutdown(self):
        self._obs_client.disconnect()

    def update_current_scene(self, event=None):
        if event is None:
            scenes = self._obs_client.call(requests.GetSceneList())
            cur_scene = scenes.getCurrentScene()
        else:
            cur_scene = event.getSceneName()
        self.current_scene = cur_scene
        self.log_scene()

    def update_camera_state(self, data=None):
        if data is None:
            for item_id in Cameras.PLAYERS:
                self._obs_client.call(requests.SetSceneItemProperties(item=item_id, visible=False))
                self.camera_state[item_id] = False
            return

        new_states = self._make_camera_state_from_data(data)
        for item_id, old_state in self.camera_state.items():
            new_state = new_states.get(item_id)
            if old_state != new_state:
                self._obs_client.call(requests.SetSceneItemProperties(item=item_id, visible=new_state))
                self.camera_state[item_id] = new_state
                print(f'OBS: {item_id} new state {new_state}')

    def prepare_team(self, side: str, team_photos: Photos):
        side_effect = 0
        if side == Sides.RADIANT:
            side_cameras = Cameras.RADIANT
            team_id = Cameras.TEAM_1
            if team_photos.TEAM_SCENE_URL == TEAM_SCENE_2_URL:
                side_effect = 5
        elif side == Sides.DIRE:
            side_cameras = Cameras.DIRE
            team_id = Cameras.TEAM_2
            if team_photos.TEAM_SCENE_URL == TEAM_SCENE_1_URL:
                side_effect = -5
        else:
            raise Exception(f'Invalid side: {side}!')

        print(side, team_photos.TEAM)
        print(
            list(enumerate(
                (
                    team_photos.POS_1_NAME,
                    team_photos.POS_2_NAME,
                    team_photos.POS_3_NAME,
                    team_photos.POS_4_NAME,
                    team_photos.POS_5_NAME,
                ), start=1
            ))
        )
        for cam_id, (name, photo) in zip(side_cameras, team_photos.ALL):
            player_id = cam_id.split('_')[1]  # player0
            ind = int(player_id[-1]) + side_effect  # 0 +5 / 5 -5
            player_id = player_id[:-1] + str(ind)  # player0/player5
            url = SOLO_URL_TEMPLATE.format(player_id, photo)

            print(name, url)
            self._obs_client.call(
                requests.SetBrowserSourceProperties(
                    source=cam_id, url=url
                )
            )

        self._obs_client.call(
            requests.SetBrowserSourceProperties(
                source=team_id, url=team_photos.TEAM_SCENE_URL
            )
        )

    def process_request(self, data):
        game_state = data.get('map', {}).get("game_state")
        callback = self.callbacks.get(game_state, self._callback_do_nothing)
        return callback(data)

    def _callback_do_nothing(self, data):
        pass

    def _callback_idle(self, data):
        if self.current_scene != Scenes.IDLE:
            self._obs_client.call(
                requests.SetCurrentScene(scene_name=Scenes.IDLE)
            )
            self.current_scene = Scenes.IDLE
            self.log_scene()

    def _callback_picks(self, data):
        if self.current_scene != Scenes.PICKS:
            self._obs_client.call(
                requests.SetCurrentScene(scene_name=Scenes.PICKS)
            )
            self.current_scene = Scenes.PICKS
            self.log_scene()

    def _callback_clean_game(self, data):
        if self.current_scene != Scenes.CLEAN_GAME:
            self._obs_client.call(
                requests.SetCurrentScene(scene_name=Scenes.CLEAN_GAME)
            )
            self.current_scene = Scenes.CLEAN_GAME
            self.log_scene()

    def _callback_game(self, data):
        if self.current_scene != Scenes.GAME:
            self._obs_client.call(
                requests.SetCurrentScene(scene_name=Scenes.GAME)
            )
            self.current_scene = Scenes.GAME

        self.update_camera_state(data)

    def log_scene(self):
        print(f'OBS: current_scene = {self.current_scene}')

    @staticmethod
    def _make_camera_state_from_data(data):
        state = {}
        hero = data['hero']
        for team_id, team_data in hero.items():
            for p_id, p_data in team_data.items():
                state[Cameras.get_camera_id_by_gsi(p_id)] = p_data["selected_unit"]
        return state


async def handler(request):
    data = await request.json()
    request.app.obs.process_request(data)
    return web.Response(text="ok")


async def on_startup(app):
    app.obs = OBS()
    app.obs.init()


async def on_cleanup(app):
    app.obs.shutdown()


async def init():
    app = web.Application()
    app.router.add_post('/', handler)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == '__main__':
    web.run_app(init(), port=3001)
