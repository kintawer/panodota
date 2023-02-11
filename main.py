from aiohttp import web
from obswebsocket import obsws, requests, events

OBS_HOST = "localhost"
OBS_PORT = 4444
OBS_PASSWORD = "secret"


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
    PLAYERS = (
        PLAYER_0, PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4,
        PLAYER_5, PLAYER_6, PLAYER_7, PLAYER_8, PLAYER_9,
    )

    @staticmethod
    def get_camera_id_by_gsi(gsi_player_id):
        return f'camera_{gsi_player_id}'


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


web.run_app(init(), port=3001)
