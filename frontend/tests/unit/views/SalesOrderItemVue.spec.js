import { mount } from '@vue/test-utils'
import SalesOrderItemVue from '@/views/SalesOrderItem.vue'

describe('SalesOrderItemVue.vue', () => {
  it('renders data.page when passed',  async () => {
    const page_data = 1
    const wrapper = mount(SalesOrderItemVue)
    await wrapper.setData({ page: page_data })
    expect(wrapper.vm.page).toBe(page_data)
  });
  it('renders data.pagination when passed',  async () => {
    const pagination_data = {
            'page':1,
            'pages':1,
            'count':0,
            'per_page':0,
          }
    const wrapper = mount(SalesOrderItemVue)
    await wrapper.setData({ pagination : pagination_data })
    expect(wrapper.vm.pagination).toEqual(pagination_data)
  });
})