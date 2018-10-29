import React from 'react'
import { shallow } from 'enzyme'
import renderer from 'react-test-renderer'

import UserList from '../UsersList'

const users = [
  {
    active: true,
    email: 'yves@yves.de',
    id: 1,
    username: 'yves',
  },
  {
    active: true,
    email: 'yves2@yves.de',
    id: 2,
    username: 'yves2',
  },
]

test('UserList renders', () => {
  const wrapper = shallow(<UserList users={users} />);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('yves');
})

test('UserList renders snapshot', () => {
  const tree = renderer.create(<UserList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot()
})
