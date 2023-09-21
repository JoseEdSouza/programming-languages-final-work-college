import sqlite3
from dataclasses import dataclass, field
from typing import List
import cmd


# The above code is defining a class called "Jogador" using the dataclass decorator. The class has
# four attributes: "id" (an integer), "nome" (a string), "apelido" (a string), and "nivel" (an
# integer).
@dataclass
class Jogador:
    id: int
    nome: str
    apelido: str
    nivel: int


@dataclass
# The class "Time" represents a team with an ID, name, number of players, and a goalkeeper.
class Time:
    id: int
    nome: str
    qntd_players: int
    goleiro: Jogador = None
    jogadores: List[Jogador] = field(default_factory=lambda: [])


# The above code is defining a class called `Racha` using the `dataclass` decorator. The `Racha` class
# has three attributes: `id` (an integer), `data` (a string), and `local` (a string).
@dataclass
class Racha:
    id: int
    data: str
    local: str


class SistemaFutebol:
    def __init__(self):
        self.conn = sqlite3.connect('racha.db')
        self.criar_tabelas()
        self.jogadores = []
        self.times = []
        self.rachas = []

    def criar_tabelas(self):
        """
        The function creates several tables in a database, including tables for players, teams, matches,
        and scores.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            PRAGMA foreign_keys = ON;""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jogador (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                apelido VARCHAR(50) NOT NULL,
                nivel INTEGER
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS time (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                qntd_players INTEGER NOT NULL
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS racha (
                id INTEGER PRIMARY KEY,
                data TEXT,
                local VARCHAR
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS time_jogadores (
                time_id INTEGER,
                jogador_id INTEGER,
                FOREIGN KEY (time_id) REFERENCES time(id),
                FOREIGN KEY (jogador_id) REFERENCES jogador(id),
                PRIMARY KEY (time_id, jogador_id)
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partida (
                id INTEGER PRIMARY KEY,
                time_1_id INTEGER NOT NULL,
                time_2_id INTEGER NOT NULL,
                racha_id INTEGER NOT NULL,
                FOREIGN KEY (time_1_id) REFERENCES time(id),
                FOREIGN KEY (time_2_id) REFERENCES time(id),
                FOREIGN KEY (racha_id) REFERENCES racha(id)
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS placar (
                partida_id INTEGER,
                time_id INTEGER,
                score INTEGER DEFAULT 0 NOT NULL,
                FOREIGN KEY (partida_id) REFERENCES partida(id),
                FOREIGN KEY (time_id) REFERENCES time(id),
                PRIMARY KEY (partida_id, time_id)
            );
        """)
        self.conn.commit()

    def cadastrar_jogador(self, nome: str, apelido: str, nivel: int):
        """
        The function `cadastrar_jogador` inserts a new player into a database table and adds the player
        to a list of players.
        
        :param nome: The parameter "nome" represents the name of the player being registered
        :type nome: str
        :param apelido: The parameter "apelido" is a string that represents the nickname of the player
        :type apelido: str
        :param nivel: The parameter "nivel" represents the level of the player. It is an integer value
        that indicates the skill level or proficiency of the player
        :type nivel: int
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO jogador (nome, apelido, nivel) VALUES (?, ?, ?)", (nome, apelido, nivel))
        jogador_id = cursor.lastrowid
        self.conn.commit()
        jogador = Jogador(jogador_id, nome, apelido, nivel)
        self.jogadores.append(jogador)
        print(f"Jogador '{nome}' cadastrado com sucesso!")

    def atribuir_nivel(self, jogador_id: int, nivel: int):
        """
        The function `atribuir_nivel` updates the level of a player in a database and also updates the
        level of the player object in memory.
        
        :param jogador_id: The jogador_id parameter is an integer that represents the unique identifier
        of a player in the database
        :type jogador_id: int
        :param nivel: The parameter "nivel" represents the level that you want to assign to a player
        :type nivel: int
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE jogador SET nivel = ? WHERE id = ?", (nivel, jogador_id))
        self.conn.commit()
        jogador = next((j for j in self.jogadores if j.id == jogador_id), None)
        if jogador:
            jogador.nivel = nivel
            print(f"Nível do jogador '{jogador.nome}' atualizado para{nivel}")

    def montar_racha(self, data: str, local: str, num_jogadores_linha: int):
        """
        The function "montar_racha" creates teams for a soccer match based on the given parameters.
        
        :param data: The "data" parameter is a string that represents the date of the racha (a soccer
        match)
        :type data: str
        :param local: The "local" parameter in the given code represents the location or venue where the
        racha (a type of soccer match) will take place. It is a string that specifies the location of
        the racha
        :type local: str
        :param num_jogadores_linha: The parameter `num_jogadores_linha` represents the number of players
        per line in a team. It is used to determine the number of teams that will be formed in the racha
        (a soccer match) and the number of players in each team
        :type num_jogadores_linha: int
        :return: The function does not have a return statement.
        """
        if len(self.jogadores) == 0:
            print("Não há jogadores cadastrados.")
            return

        if num_jogadores_linha <= 0:
            print("Número inválido de jogadores por time.")
            return

        jogadores_disponiveis = sorted(
            self.jogadores, key=lambda jogador: jogador.nivel, reverse=True)
        num_jogadores = min(len(jogadores_disponiveis), (num_jogadores_linha+1)
                            * len(jogadores_disponiveis) // num_jogadores_linha)
        num_times = num_jogadores // (num_jogadores_linha+1)
        jogadores_selecionados = jogadores_disponiveis[:num_jogadores]
        goleiros = jogadores_selecionados[:num_times]
        jogadores_linha = jogadores_selecionados[num_times:]

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO racha (data, local) VALUES (?, ?)", (data, local))
        racha_id = cursor.lastrowid
        self.conn.commit()

        times = []
        for i in range(num_times):
            cursor.execute("INSERT INTO time (nome, qntd_players) VALUES (?, ?)",
                           (f"Time {i+1}", num_jogadores_linha))
            time_id = cursor.lastrowid
            self.conn.commit()
            times.append(Time(time_id, f"Time {i+1}", num_jogadores_linha))

        for i, (time, goleiro) in enumerate(zip(times, goleiros)):
            cursor.execute(
                "INSERT INTO time_jogadores (time_id, jogador_id) VALUES (?, ?)", (time.id, goleiro.id))
            self.conn.commit()
            time.goleiro = goleiro

        for i, (time, jogador) in enumerate(zip(times * num_jogadores_linha, jogadores_linha)):
            cursor.execute(
                "INSERT INTO time_jogadores (time_id, jogador_id) VALUES (?, ?)", (time.id, jogador.id))
            self.conn.commit()
            time.jogadores.append(jogador)

        racha = Racha(racha_id, data, local)
        self.rachas.append(racha)
        print("Racha montado com sucesso!")

    def registrar_placar(self, racha_id: int, time_id: int, score: int):
        """
        The function `registrar_placar` inserts a score into the "placar" table in a database,
        associating it with a specific "racha_id" and "time_id".
        
        :param racha_id: The `racha_id` parameter represents the ID of the match or game
        :type racha_id: int
        :param time_id: The `time_id` parameter represents the ID of the team for which the score is
        being registered
        :type time_id: int
        :param score: The "score" parameter represents the score achieved by a team in a particular
        match
        :type score: int
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO placar (partida_id, time_id, score) VALUES (?, ?, ?)", (racha_id, time_id, score))
        self.conn.commit()
        print("Placar registrado com sucesso!")

    def carregar_jogadores(self):
        """
        The function "carregar_jogadores" retrieves player data from a database and stores it in a list
        of player objects.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, apelido, nivel FROM jogador")
        rows = cursor.fetchall()
        self.jogadores = [Jogador(*row) for row in rows]

    def carregar_times(self):
        """
        The function `carregar_times` retrieves data from the database and populates a list of `Time`
        objects, each containing information about a team and its players.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, qntd_players FROM time")
        rows = cursor.fetchall()
        self.times = [Time(id=row[0], nome=row[1], qntd_players=row[2])
                      for row in rows]

        for time in self.times:
            cursor.execute(
                "SELECT jogador_id FROM time_jogadores WHERE time_id = ?", (time.id,))
            jogador_ids = [jogador_id[0] for jogador_id in cursor.fetchall()]
            time.jogadores = [
                jogador for jogador in self.jogadores if jogador.id in jogador_ids]

    def carregar_rachas(self):
        """
        The function "carregar_rachas" retrieves data from a database table called "racha" and stores it
        in a list of objects called "rachas".
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, data, local FROM racha")
        rows = cursor.fetchall()
        self.rachas = [Racha(*row) for row in rows]

    def salvar_dados(self):
        """
        The function saves data and prints a success message.
        """
        self.conn.commit()
        print("Dados salvos com sucesso!")

    def carregar_dados(self):
        """
        The function "carregar_dados" loads data from a database, including players, teams, and matches.
        """
        self.carregar_jogadores()
        self.carregar_times()
        self.carregar_rachas()
        print("Dados carregados do banco de dados.")

    def listar_jogadores(self):
        """
        The function "listar_jogadores" prints the information of all registered players.
        """
        print("Jogadores cadastrados:")
        for jogador in self.jogadores:
            print(
                f"ID: {jogador.id}, Nome: {jogador.nome}, Apelido: {jogador.apelido}, Nível: {jogador.nivel}")
        print()

    def listar_rachas(self):
        """
        The function "listar_rachas" prints the registered rachas with their respective ID, date, and
        location.
        """
        print("Rachas registrados:")
        for racha in self.rachas:
            print(f"ID: {racha.id}, Data: {racha.data}, Local: {racha.local}")
        print()

    def listar_times(self):
        """
        The function `listar_times` prints the names of teams and their players, including the
        goalkeeper if available.
        """
        print("Times e seus jogadores:")
        for time in self.times:
            print(f"Time: {time.nome}")
            print("Jogadores:")
            for jogador in time.jogadores:
                print(
                    f"- {jogador.nome} ({jogador.apelido}) - Nível: {jogador.nivel}")
            if time.goleiro != None:
                print(
                    f"- {time.goleiro.nome} ({time.goleiro.apelido}) - Nível: {time.goleiro.nivel}")
            print()

    def deletar_racha(self, racha_id):
        """
        The function deletes a "racha" (a type of object) from a list and a database, and prints a
        success message if the deletion is successful.
        
        :param racha_id: The `racha_id` parameter is the unique identifier of the racha that needs to be
        deleted. It is used to find the racha object in the `self.rachas` list and also to delete the
        corresponding record from the `racha` table in the database
        """
        racha = next((r for r in self.rachas if r.id == racha_id), None)
        if racha:
            self.rachas.remove(racha)
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM racha WHERE id = ?", (racha_id,))
            self.conn.commit()
            print("Racha removido com sucesso!")
            self.carregar_dados()
        else:
            print("Racha não encontrado!")

    def deletar_time(self, time_id):
        """
        The function `deletar_time` deletes a team from a database and prints a success message if the
        team is found, or a not found message if the team is not found.
        
        :param time_id: The `time_id` parameter is the unique identifier of the time (team) that you
        want to delete
        """
        time = next((t for t in self.times if t.id == time_id), None)
        if time:
            self.times.remove(time)
            cursor = self.conn.cursor()

            cursor.execute(
                "DELETE FROM time_jogadores WHERE time_id = ?", (time_id,))
            cursor.execute("DELETE FROM time WHERE id = ?", (time_id,))
            self.conn.commit()
            print("Time removido com sucesso!")
            self.carregar_dados()
        else:
            print("Time não encontrado!")

    def deletar_jogador(self, jogador_id):
        """
        The function `deletar_jogador` deletes a player from a database and updates the data.
        
        :param jogador_id: The `jogador_id` parameter is the unique identifier of the player that you
        want to delete from the system
        """
        jogador = next((j for j in self.jogadores if j.id == jogador_id), None)
        if jogador:
            self.jogadores.remove(jogador)
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM time_jogadores WHERE jogador_id = ?", (jogador_id,))
            cursor.execute("DELETE FROM jogador WHERE id = ?", (jogador_id,))
            self.conn.commit()
            print("Jogador removido com sucesso!")
            self.carregar_dados()
        else:
            print("Jogador não encontrado!")

    def encerrar_conexao(self):
        """
        The function "encerrar_conexao" closes the connection.
        """
        self.conn.close()


# The `InterfaceTerminal` class is a command-line interface that allows users to interact with a
# `sistema` object by executing various commands.
class InterfaceTerminal(cmd.Cmd):
    prompt = ">>> "

    def __init__(self, sistema):
        super().__init__()
        self.sistema = sistema

    def do_cadastrar_jogador(self, args):
        """
        The function "do_cadastrar_jogador" prompts the user to input the name, nickname, and level of a
        player, and then calls the "cadastrar_jogador" method of the "sistema" object to register the
        player.
        
        :param args: The "args" parameter is a placeholder for any additional arguments that may be
        passed to the "do_cadastrar_jogador" method. It is not used in the provided code snippet
        """
        nome = input("Nome do jogador: ")
        apelido = input("Apelido do jogador: ")
        nivel = int(input("Nível do jogador (1-5): "))
        self.sistema.cadastrar_jogador(nome, apelido, nivel)

    def do_atribuir_nivel(self, args):
        """
        The function "do_atribuir_nivel" prompts the user to enter a player ID and a new level for the
        player, and then calls the "atribuir_nivel" method of the "sistema" object with the provided
        arguments.
        
        :param args: The "args" parameter is not used in the given code snippet. It is present in the
        function definition but not used within the function body
        """
        jogador_id = int(input("ID do jogador: "))
        nivel = int(input("Novo nível do jogador (1-5): "))
        self.sistema.atribuir_nivel(jogador_id, nivel)

    def do_montar_racha(self, args):
        """
        The function "do_montar_racha" prompts the user for input regarding the date, location, and
        number of players per line for a soccer match, and then calls the "montar_racha" method of the
        "sistema" object with the provided information.
        
        :param args: The `args` parameter is not used in the `do_montar_racha` method. It is included in
        the method signature but not used within the method body
        """
        data = input("Data do racha: ")
        local = input("Local do racha: ")
        num_jogadores_linha = int(input("Número de jogadores por linha: "))
        self.sistema.montar_racha(data, local, num_jogadores_linha)

    def do_registrar_placar(self, args):
        """
        The function `do_registrar_placar` prompts the user for the ID of a "racha" (match), the ID of a
        team, and the score, and then calls the `registrar_placar` method of the `sistema` object with
        these values.
        
        :param args: The "args" parameter is not used in the code snippet you provided. It seems to be
        unused and can be removed from the function definition
        """
        racha_id = int(input("ID do racha: "))
        time_id = int(input("ID do time: "))
        score = int(input("Placar: "))
        self.sistema.registrar_placar(racha_id, time_id, score)

    def do_listar_jogadores(self, args):
        """
        The function "do_listar_jogadores" calls the "listar_jogadores" method of the "sistema" object.
        
        :param args: The "args" parameter is a placeholder for any additional arguments that may be
        passed to the "do_listar_jogadores" method. It can be used to provide additional information or
        configuration options to the method
        """
        self.sistema.listar_jogadores()

    def do_listar_rachas(self, args):
        """
        The function "do_listar_rachas" calls the "listar_rachas" method of the "sistema" object.
        
        :param args: The "args" parameter is a placeholder for any additional arguments that may be
        passed to the "do_listar_rachas" method. It can be used to pass any necessary information or
        configuration options to the method
        """
        self.sistema.listar_rachas()

    def do_listar_times(self, args):
        """
        The function "do_listar_times" calls the "listar_times" method of the "sistema" object.
        
        :param args: The parameter "args" is likely a placeholder for any additional arguments that may
        be passed to the "do_listar_times" method. It could be used to pass any necessary information or
        configuration options to the method
        """
        self.sistema.listar_times()

    def do_deletar_racha(self, args):
        """
        The function `do_deletar_racha` prompts the user for the ID of a "racha" (a term that is not
        defined in the code) to be deleted, and then calls the `deletar_racha` method of the `sistema`
        object with the provided ID.
        
        :param args: The "args" parameter is not used in the code snippet you provided. It is common to
        use the "args" parameter to pass additional arguments to a function, but in this case, it is not
        being used
        """
        racha_id = int(input("ID da racha a ser deletada: "))
        self.sistema.deletar_racha(racha_id)

    def do_deletar_time(self, args):
        """
        The function `do_deletar_time` prompts the user for the ID of a team to be deleted and calls the
        `deletar_time` method of the `sistema` object to delete the team.
        
        :param args: The "args" parameter is not used in the given code snippet. It is present as a
        placeholder for any additional arguments that may be passed to the function
        """
        time_id = int(input("ID do time a ser deletado: "))
        self.sistema.deletar_time(time_id)

    def do_deletar_jogador(self, args):
        """
        The function `do_deletar_jogador` prompts the user for an ID and then calls the
        `deletar_jogador` method of the `sistema` object with that ID as an argument.
        
        :param args: The "args" parameter is not used in the given code snippet. It is defined in the
        function signature but not used within the function body
        """
        jogador_id = int(input("ID do jogador a ser deletado: "))
        self.sistema.deletar_jogador(jogador_id)

    def do_help(self, args):
        """
        The `do_help` function prints a list of available commands and their descriptions.
        
        :param args: The `args` parameter is a list of arguments passed to the `do_help` method. It can
        be used to provide additional information or context for the help command
        """
        print("""
Comandos disponíveis:
- cadastrar_jogador: Cadastra um novo jogador.
- atribuir_nivel: Atribui um novo nível a um jogador existente.
- montar_racha: Monta um novo racha com os jogadores cadastrados.
- registrar_placar: Registra o placar de um racha.
- listar_jogadores: Lista todos os jogadores cadastrados.
- listar_rachas: Lista todos os rachas registrados.
- listar_times: Lista todos os times e seus joagores.
- deletar_racha: Deleta o racha referente ao id fornecido.
- deletar_time: Deleta o time referente ao id fornecido.
- deletar_racha: Deleta o jogador referente ao id fornecido.
- help: Exibe esta mensagem de ajuda.
- quit: Encerra o programa.
""")

    def do_quit(self, args):
        """
        The function "do_quit" saves data, closes the connection, prints a message, and returns True to
        indicate that the program is being terminated.
        
        :param args: The "args" parameter is a placeholder for any additional arguments that may be
        passed to the "do_quit" method. In this case, it seems that no arguments are being passed to the
        method
        :return: True.
        """
        self.sistema.salvar_dados()
        self.sistema.encerrar_conexao()
        print("Encerrando o programa...")
        return True

    def emptyline(self):
        pass


if __name__ == "__main__":
    # The above code is creating an instance of the `SistemaFutebol` class and calling its
    # `carregar_dados()` method to load data. It then creates an instance of the `InterfaceTerminal`
    # class, passing the `sistema` object as an argument. Finally, it starts a command loop for the
    # terminal interface with a welcome message.
    sistema = SistemaFutebol()
    sistema.carregar_dados()

    interface = InterfaceTerminal(sistema)
    interface.cmdloop(
        "Bem-vindo ao sistema de gerenciamento de times de futebol da UFC!")
