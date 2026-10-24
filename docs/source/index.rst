SCARA Robot Python Emulator & 2D/3D Kinematic Visualizer
---------------------------------------------------------

**scaraemu** is a standalone kinematic emulator, real-time 2D/3D visualizer, and hardware communication bridge for 4-DOF SCARA robotic manipulators.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|scaraemu python checker| |scaraemu python package| |scaraemu interface checker| |scaraemu isp checker| |scaraemu srp checker| |gplv3 license| |apache license| |python version| |github issues| |documentation status| |github contributors|

.. |scaraemu python checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python_checker.yml

.. |scaraemu python package| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_package.yml

.. |scaraemu interface checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_interface_checker.yml

.. |scaraemu isp checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_isp_checker.yml

.. |scaraemu srp checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_srp_checker.yml

.. |gplv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |apache license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |python version| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/scaraemu.svg
   :target: https://github.com/vroncevic/scaraemu/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/scaraemu.svg
   :target: https://github.com/vroncevic/scaraemu/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/scaraemu/badge/?version=latest
   :target: https://scaraemu.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|scaraemu python3 build|

.. |scaraemu python3 build| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/scaraemu/releases

To install **scaraemu** type the following

.. code-block:: bash

    tar xvzf scaraemu-x.y.z.tar.gz
    cd scaraemu-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/scaraemu-*-py3-none-any.whl
    rm -f get-pip.py
    chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/scaraemu_run.py
    ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/scaraemu_run.py /usr/local/bin/scaraemu_run.py

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # python3
    pip3 install scaraemu

📦 Dependencies
---------------

**scaraemu** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_ |ats gplv3| |ats apache|
* `pyserial - Python Serial Port Extension <https://pypi.org/project/pyserial/>`_ |pyserial bsd|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |pyserial bsd| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

📁 Tool structure
-----------------

**scaraemu** is based on OOP and Hexagonal Architecture.

Tool structure

.. code-block:: bash

    scaraemu/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── __init__.py
         │   │   │   ├── joints.py
         │   │   │   ├── pose.py
         │   │   │   └── step_coords.py
         │   │   └── simulation/
         │   │       ├── __init__.py
         │   │       ├── state.py
         │   │       └── telemetry.py
         │   └── service/
         │       ├── emulation/
         │       │   ├── controller/
         │       │   │   ├── controller.py
         │       │   │   ├── flags.py
         │       │   │   ├── icontroller.py
         │       │   │   └── __init__.py
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── iservice.py
         │       │   ├── motion/
         │       │   │   ├── __init__.py
         │       │   │   └── stepper.py
         │       │   ├── notification/
         │       │   │   ├── ilistener.py
         │       │   │   ├── __init__.py
         │       │   │   ├── inotifier.py
         │       │   │   └── notifier.py
         │       │   ├── provides.py
         │       │   ├── queue/
         │       │   │   ├── __init__.py
         │       │   │   ├── iqueue.py
         │       │   │   ├── queue.py
         │       │   │   └── snapshot.py
         │       │   └── service.py
         │       ├── __init__.py
         │       └── kinematics/
         │           ├── imanipulator.py
         │           └── __init__.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── bundle.py
         │   │   ├── definition.py
         │   │   ├── executor.py
         │   │   ├── idefinition.py
         │   │   ├── iexecutor.py
         │   │   └── __init__.py
         │   ├── config/
         │   │   ├── scara_geometry.json
         │   │   ├── scara_geometry_scheme.json
         │   │   ├── scaraemu.cfg
         │   │   └── scaraemu.logo
         │   ├── connection/
         │   │   ├── command/
         │   │   │   ├── dependencies.py
         │   │   │   ├── dispatcher.py
         │   │   │   ├── factory.py
         │   │   │   ├── idispatcher.py
         │   │   │   └── __init__.py
         │   │   ├── coordinator/
         │   │   │   ├── coordinator.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── icoordinator.py
         │   │   │   └── __init__.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── handler/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── handler.py
         │   │   │   ├── ihandler.py
         │   │   │   └── __init__.py
         │   │   ├── __init__.py
         │   │   ├── listener/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── listener.py
         │   │   └── provides.py
         │   ├── dependencies.py
         │   ├── factory.py
         │   ├── gui/
         │   │   ├── bridge/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── log/
         │   │   │   │   ├── adapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── provides.py
         │   │   │   ├── server/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── log_adapter.py
         │   │   │   │   └── state_adapter.py
         │   │   │   ├── status/
         │   │   │   │   ├── adapter.py
         │   │   │   │   └── __init__.py
         │   │   │   └── sync/
         │   │   │       ├── __init__.py
         │   │   │       ├── isynchronizer.py
         │   │   │       └── synchronizer.py
         │   │   ├── canvas/
         │   │   │   ├── canvas_xy.py
         │   │   │   ├── canvas_z.py
         │   │   │   ├── config.py
         │   │   │   ├── icanvas_xy.py
         │   │   │   ├── icanvas_z.py
         │   │   │   ├── __init__.py
         │   │   │   ├── renderer/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── j1_boundary_renderer.py
         │   │   │   │   ├── manipulator_arm_renderer.py
         │   │   │   │   ├── manipulator_render_context.py
         │   │   │   │   ├── trail_renderer.py
         │   │   │   │   ├── trajectory_path_renderer.py
         │   │   │   │   ├── workspace_boundary_renderer.py
         │   │   │   │   ├── z_render_context.py
         │   │   │   │   └── z_renderer.py
         │   │   │   ├── target/
         │   │   │   │   ├── elbow_auto_switch_coordinator.py
         │   │   │   │   ├── elbow_dependencies.py
         │   │   │   │   ├── ielbow_auto_switch_coordinator.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── itarget_click_listener.py
         │   │   │   │   ├── itarget_motion_dispatcher.py
         │   │   │   │   ├── target_action_coordinator.py
         │   │   │   │   ├── target_dependencies.py
         │   │   │   │   └── target_motion_dispatcher.py
         │   │   │   └── viewport/
         │   │   │       ├── coordinate_transformer.py
         │   │   │       ├── icoordinate_transformer.py
         │   │   │       ├── __init__.py
         │   │   │       ├── iviewport.py
         │   │   │       ├── viewport.py
         │   │   │       └── z_coordinate_mapper.py
         │   │   ├── console/
         │   │   │   ├── buffer_actions.py
         │   │   │   ├── ilog_listener.py
         │   │   │   ├── __init__.py
         │   │   │   └── panel.py
         │   │   ├── delegates/
         │   │   │   ├── assembly.py
         │   │   │   ├── bundle.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   └── __init__.py
         │   │   ├── dependencies.py
         │   │   ├── engine.py
         │   │   ├── factory.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── jog/
         │   │   │   ├── action/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── dpad/
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   └── step/
         │   │   │       ├── __init__.py
         │   │   │       ├── iprovider.py
         │   │   │       └── section.py
         │   │   ├── layout/
         │   │   │   ├── builder/
         │   │   │   │   ├── builder.py
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ibuilder.py
         │   │   │   │   └── __init__.py
         │   │   │   └── __init__.py
         │   │   ├── lifecycle/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── irunner.py
         │   │   │   └── runner.py
         │   │   ├── machine/
         │   │   │   ├── configuration/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   └── safety/
         │   │   │       ├── coordinator.py
         │   │   │       ├── idelegate.py
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   ├── provides.py
         │   │   ├── services.py
         │   │   ├── splash/
         │   │   │   ├── factory.py
         │   │   │   ├── ifactory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iscreen.py
         │   │   │   └── screen.py
         │   │   ├── telemetry/
         │   │   │   ├── cartesian/
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iview.py
         │   │   │   ├── joint/
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── panel.py
         │   │   │   └── step/
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   ├── theme/
         │   │   │   ├── __init__.py
         │   │   │   ├── style.py
         │   │   │   └── theme.py
         │   │   ├── ticker/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── ifactory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iticker.py
         │   │   │   ├── observer/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── iobserver.py
         │   │   │   │   └── observer.py
         │   │   │   ├── scheduler/
         │   │   │   │   ├── ilistener.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── ischeduler.py
         │   │   │   │   └── scheduler.py
         │   │   │   └── ticker.py
         │   │   ├── toolbar/
         │   │   │   ├── action/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── connection/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── istatus_view.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   ├── port/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── iprovider.py
         │   │   │   │   └── section.py
         │   │   │   └── server/
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   ├── trajectory/
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   ├── preset/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── queue/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── iview.py
         │   │   │   │   └── section.py
         │   │   │   └── script/
         │   │   │       ├── coordinator.py
         │   │   │       ├── idelegate.py
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   └── window/
         │   │       ├── configurator.py
         │   │       ├── factory.py
         │   │       ├── iconfigurator.py
         │   │       └── __init__.py
         │   ├── __init__.py
         │   ├── preferences/
         │   │   ├── dependencies.py
         │   │   ├── exceptions/
         │   │   │   ├── __init__.py
         │   │   │   └── preference_not_found_error.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   ├── serial/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── repository.py
         │   │   └── server/
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── irepository.py
         │   │       ├── preference.py
         │   │       └── repository.py
         │   ├── provides.py
         │   ├── scaralang/
         │   │   ├── bypass/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── demo/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── __init__.py
         │   │   │   ├── linkage/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   └── solver/
         │   │   │       ├── adapter.py
         │   │   │       ├── factory.py
         │   │   │       ├── iadapter.py
         │   │   │       └── __init__.py
         │   │   ├── protocol/
         │   │   │   ├── builder/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── codec/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── payload/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── provides.py
         │   │   │   └── response/
         │   │   │       ├── adapter.py
         │   │   │       ├── factory.py
         │   │   │       ├── iadapter.py
         │   │   │       └── __init__.py
         │   │   ├── provides.py
         │   │   ├── reach/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── safety/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   └── script/
         │   │       ├── adapter.py
         │   │       ├── discovery.py
         │   │       ├── factory.py
         │   │       ├── iadapter.py
         │   │       └── __init__.py
         │   ├── server/
         │   │   ├── accept/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iworker.py
         │   │   │   └── worker.py
         │   │   ├── dependencies.py
         │   │   ├── dispatcher/
         │   │   │   ├── dispatcher.py
         │   │   │   ├── factory.py
         │   │   │   ├── idispatcher.py
         │   │   │   └── __init__.py
         │   │   ├── factory.py
         │   │   ├── handler/
         │   │   │   ├── ihandler.py
         │   │   │   ├── __init__.py
         │   │   │   ├── jog/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── motion/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── system/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   └── __init__.py
         │   │   │   └── tool/
         │   │   │       ├── dependencies.py
         │   │   │       ├── factory.py
         │   │   │       ├── handler.py
         │   │   │       └── __init__.py
         │   │   ├── __init__.py
         │   │   ├── iserver.py
         │   │   ├── logger/
         │   │   │   ├── factory.py
         │   │   │   ├── holder.py
         │   │   │   ├── iholder.py
         │   │   │   ├── ilistener.py
         │   │   │   └── __init__.py
         │   │   ├── manager/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── ilistener.py
         │   │   │   ├── imanager.py
         │   │   │   ├── __init__.py
         │   │   │   └── manager.py
         │   │   ├── motion_completion_listener.py
         │   │   ├── pose/
         │   │   │   ├── factory.py
         │   │   │   ├── holder.py
         │   │   │   ├── iholder.py
         │   │   │   └── __init__.py
         │   │   ├── processor/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iprocessor.py
         │   │   │   └── processor.py
         │   │   ├── provides.py
         │   │   ├── server.py
         │   │   └── session/
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── ioutbound_queue.py
         │   │       ├── iworker.py
         │   │       ├── outbound_queue.py
         │   │       └── worker.py
         │   ├── settings/
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── geometry/
         │   │   │   ├── factory.py
         │   │   │   ├── iloader.py
         │   │   │   ├── __init__.py
         │   │   │   └── loader.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   └── transmission/
         │   │       ├── factory.py
         │   │       ├── iloader.py
         │   │       ├── __init__.py
         │   │       └── loader.py
         │   └── streaming/
         │       ├── dependencies.py
         │       ├── factory.py
         │       ├── __init__.py
         │       ├── motion/
         │       │   ├── coordinator.py
         │       │   ├── factory.py
         │       │   ├── icoordinator.py
         │       │   └── __init__.py
         │       ├── provides.py
         │       ├── pumper/
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── ipumper.py
         │       │   └── pumper.py
         │       └── streamer/
         │           ├── dependencies.py
         │           ├── factory.py
         │           ├── __init__.py
         │           ├── istreamer.py
         │           └── streamer.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── kinematics/
             │   ├── dependencies.py
             │   ├── factory.py
             │   ├── __init__.py
             │   └── provides.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     103 directories, 408 files

✨ Features
-----------

* **2D Planar Dual-Link Visualizer**: Real-time rendering of primary ($L_1$) and secondary ($L_2$) arm links, active joint angles, target crosshair, and animated motion path trail.
* **Side Elevation Z-Tower View**: Multi-rod lead screw carriage elevation, active tool height, and radial extension profile visualization.
* **Interactive Targeting & Jogging**: Direct mouse click position targeting on both XY and Z canvases, Cartesian delta jogging ($X, Y, Z, \Phi$), Lefty/Righty elbow toggling, and Emergency Stop.
* **Autonomous Trajectory Demos**: Pre-programmed autonomous demonstration trajectories (Circle, Square, 5-Point Star, 3D Helical Coil).
* **Virtual Server Bridge & Binary Protocol Codec**: Bidirectional streaming over TCP socket (port 8888) with ``scaralang`` binary wire frames (``0xAA 0x55``), console log, and real-time status telemetry queries.
* **Configurable Kinematics & Dimensions**: Dynamic robot link lengths ($L_1, L_2$), stroke limits ($Z_{min}, Z_{max}$), and speed bounds configurable via CLI options and JSON schema.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, 100% code coverage (8,947/8,947 lines), and 9.99 / 10.00 Pylint score.

📐 SCARA Kinematic & Geometric Configuration
--------------------------------------------

The robot dimensions and physical boundaries can be customized in ``scara_geometry.json`` or injected programmatically:

.. list-table:: Kinematic Limits
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Default Value
     - Description
   * - **l1**
     - ``150.0 mm``
     - Primary arm link length (shoulder to elbow).
   * - **l2**
     - ``120.0 mm``
     - Secondary arm link length (elbow to wrist).
   * - **r_min**
     - ``30.0 mm``
     - Inner singular deadzone radius (:math:`|L_1 - L_2|`).
   * - **r_max**
     - ``270.0 mm``
     - Maximum horizontal reach boundary (:math:`L_1 + L_2`).
   * - **z_min**
     - ``0.0 mm``
     - Minimum vertical height limit (bed level).
   * - **z_max**
     - ``100.0 mm``
     - Maximum vertical stroke limit.
   * - **min_speed**
     - ``1.0 mm/s``
     - Minimum allowable feedrate speed.
   * - **max_speed**
     - ``100.0 mm/s``
     - Maximum allowable safe feedrate speed.

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install scaraemu

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/scaraemu/main/main.py

CLI Command Options
^^^^^^^^^^^^^^^^^^^

Launch the graphical emulator with default configuration:

.. code-block:: bash

    python3 main.py emulator

Launch with custom geometry overrides:

.. code-block:: bash

    python3 main.py emulator --l1 160.0 --l2 110.0 --verbose

.. list-table:: Emulator CLI Options
   :widths: 20 15 25 40
   :header-rows: 1

   * - Option
     - Type
     - Choices
     - Description
   * - **--l1**
     - ``float``
     - *Length in mm*
     - Override primary arm length L1 in millimeters.
   * - **--l2**
     - ``float``
     - *Length in mm*
     - Override secondary arm length L2 in millimeters.
   * - **--z-min**
     - ``float``
     - *Limit in mm*
     - Minimum vertical Z boundary in millimeters.
   * - **--z-max**
     - ``float``
     - *Limit in mm*
     - Maximum vertical Z boundary in millimeters.
   * - **--robot-config**
     - ``str``
     - *File path*
     - Path to custom robot geometry JSON file.
   * - **--verbose**
     - ``bool``
     - *Flag*
     - Enable verbose ATS operational logging.

Interactive Emulation & Control Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **2D/3D Kinematic Visualizer**:
   * Inspect top-down planar canvas (XY) and side elevation carriage (Z).
   * Directly click anywhere inside reachable annular workspace to command moves.
2. **Manual Jogging & Axis Control**:
   * Step along :math:`X, Y, Z, \Phi` with configurable step sizes under **Monitor & Jog**.
   * Toggle between Lefty and Righty elbow configurations or toggle motor power.
3. **Autonomous Demo Trajectories**:
   * Under the **Trajectories** tab, select **Circle**, **Square**, **5-Star**, or **3D Helix**.
   * Watch the real-time simulation interpolator render toolhead paths.
4. **Virtual Server & Telemetry Streaming**:
   * Run embedded Virtual Robot Server listening on TCP socket ``127.0.0.1:8888``.
   * Telemetry updates synchronize simulated robot position with the visualizer.
5. **Console & Telemetry Logging**:
   * Inspect live binary protocol logs, server communication events, and real-time telemetry updates.

🤖 Digital Twin Integration with SCARAjectory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**scaraemu** acts as a virtual hardware target, SITL digital twin, and kinematic simulator for `scarajectory <https://github.com/vroncevic/scarajectory>`_.

Method 1: Virtual Robot Server (TCP 127.0.0.1:8888)
"""""""""""""""""""""""""""""""""""""""""""""""""""

1. In **scaraemu**, click the **🌐 Virtual Server: OFF** toggle button on the top status bar.
2. The button illuminates green and displays **🌐 Virtual Server: 8888**, listening for incoming TCP client connections on ``127.0.0.1:8888``.
3. In **scarajectory**, navigate to the **Hardware Streamer** tab and select **127.0.0.1:8888 (Digital Twin)** from the Port dropdown.
4. Click **Connect** in **scarajectory**.
5. Stream any trajectory plan or jog joints interactively:
   * **scaraemu** decodes incoming ``scaralang`` binary motion frames (``CMD_MOVE_JOINT_STEPS``).
   * Forward kinematics computes joint angles (:math:`\theta_1, \theta_2, Z, \phi`) and renders real-time motion on the 2D and 3D canvases.
   * Bidirectional handshake frames (``RESP_ACK``, ``RESP_MOVE_DONE``) flow back to **scarajectory** for closed-loop motion synchronization.

Method 2: Launch via CLI with Initial File
""""""""""""""""""""""""""""""""""""""""""

Launch **scaraemu** with an initial ``.scara`` script or ``plan.json``:

.. code-block:: bash

    python3 main.py emulator --file /path/to/trajectory.scara

The emulator automatically loads the file, executes forward and inverse kinematics, and displays the toolhead path.

Method 3: Load .scara DSL Programs from UI
""""""""""""""""""""""""""""""""""""""""""

1. Navigate to the **Trajectories** tab in **scaraemu**.
2. Select any program from the **SCARA DSL Script** dropdown (12 industrial demo programs included).
3. Or click **📂 Load** to browse and open any custom ``.scara`` or JSON trajectory plan.

📚 Docs
-------

More documentation and info at

* `scaraemu.readthedocs.io <https://scaraemu.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to scaraemu <https://github.com/vroncevic/scaraemu/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/scaraemu <https://vroncevic.github.io/scaraemu>`_

**scaraemu** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.python.org/psf/donations/
