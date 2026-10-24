# -*- coding: UTF-8 -*-

'''
Module
    factory.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaraemu is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaraemu is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Factory for assembling infrastructure services, communication, GUI, and CLI.
'''

from __future__ import annotations

from scaracom.transport.factory import TransportFactory
from scaracom.transport.itransport import ITransport
from scaracom.transport.scanner.factory import PortScannerFactory
from scaracom.transport.scanner.iport_scanner import IPortScanner

from scaraemu.infrastructure.cli.engine import CLI
from scaraemu.infrastructure.cli.icli import ICLI
from scaraemu.infrastructure.cli.setup.bundle import CLIBundle
from scaraemu.infrastructure.cli.setup.factory import CLIBundleFactory
from scaraemu.infrastructure.cli.setup.options import CLIBundleOptions
from scaraemu.infrastructure.dependencies import InfrastructureDependencies
from scaraemu.infrastructure.gui.dependencies import GuiDependencies
from scaraemu.infrastructure.gui.factory import GuiFactory
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.gui.provides import GuiProvides
from scaraemu.infrastructure.gui.services import GuiServicesBundle
from scaraemu.infrastructure.preferences.dependencies import PreferencesDependencies
from scaraemu.infrastructure.preferences.factory import PreferencesFactory
from scaraemu.infrastructure.preferences.provides import PreferencesProvides
from scaraemu.infrastructure.provides import InfrastructureProvides
from scaraemu.infrastructure.scaralang.dependencies import ScaralangDependencies
from scaraemu.infrastructure.scaralang.factory import ScaralangFactory
from scaraemu.infrastructure.scaralang.provides import ScaralangProvides
from scaraemu.infrastructure.server.dependencies import ServerDependencies
from scaraemu.infrastructure.server.factory import ServerFactory
from scaraemu.infrastructure.server.provides import ServerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InfrastructureFactory:
    '''
        Factory for assembling infrastructure services, communication, GUI, and CLI.

        It defines:

            :methods:
                | create - Assembles virtual server, stream transport, GUI, and CLI.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls, dependencies: InfrastructureDependencies
    ) -> InfrastructureProvides:
        '''
            Assembles virtual server, stream transport, GUI, and CLI.

            :param dependencies: Encapsulated infrastructure setup dependencies.
            :return: The assembled infrastructure provides container.
            :exceptions:
                | ATSValueError: When configuration or options are invalid.
                | ATSTypeError: When arguments do not conform to expected interfaces.
        '''
        scaralang_deps = ScaralangDependencies(bounds=dependencies.bounds)
        scaralang: ScaralangProvides = ScaralangFactory.create(
            dependencies=scaralang_deps
        )

        server_dependencies = ServerDependencies(
            emulation_controller=dependencies.emulation_controller,
            emulation_service=dependencies.emulation_service,
            emulation_queue=dependencies.emulation_queue,
            motion_notifier=dependencies.motion_notifier,
            home_pose=dependencies.home_pose,
            kinematics=dependencies.kinematics,
            motion_validator=scaralang.safety,
            response_builder=scaralang.response_builder,
            codec=scaralang.codec,
            decoder=scaralang.payload_decoder,
        )
        server: ServerProvides = ServerFactory.create(
            dependencies=server_dependencies
        )

        transport: ITransport = TransportFactory.create()

        preferences_dependencies = PreferencesDependencies(
            context_bundle=dependencies.context_bundle,
        )
        preferences: PreferencesProvides = PreferencesFactory.create(
            dependencies=preferences_dependencies,
        )

        port_scanner: IPortScanner = PortScannerFactory.create()

        services = GuiServicesBundle(
            transport=transport,
            kinematics=dependencies.kinematics,
            emulation_service=dependencies.emulation_service,
            emulation_controller=dependencies.emulation_controller,
            emulation_queue=dependencies.emulation_queue,
            server=server,
            preferences=preferences,
            scaralang=scaralang,
            port_scanner=port_scanner,
        )

        gui_deps = GuiDependencies(
            bounds=dependencies.bounds,
            services=services,
            initial_script=dependencies.initial_script_path,
        )
        gui_provides: GuiProvides = GuiFactory.create(dependencies=gui_deps)
        gui: IGUI = gui_provides.gui

        cli_bundle: CLIBundle = CLIBundleFactory.create(
            options=CLIBundleOptions(
                parser=dependencies.base_bundle.option_manager,
                launcher=gui,
            )
        )

        cli: ICLI = CLI(cli_bundle)

        return InfrastructureProvides(
            gui=gui,
            cli=cli,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
