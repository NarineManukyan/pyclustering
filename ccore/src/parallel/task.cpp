/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/


#include "task.hpp"


namespace ccore {

namespace parallel {


task::task(const proc & p_task) :
    m_task(p_task)
{ 
    m_ready.lock();
}


void task::set_ready(void) {
    m_ready.unlock();
}


void task::wait_ready(void) const {
    m_ready.lock();
}


void task::operator()() {
    m_task();
}


}

}
