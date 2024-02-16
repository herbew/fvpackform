import { mount,  shallowMount } from '@vue/test-utils'
import SalesOrderItemVue from '@/views/SalesOrderItem.vue'
import moment from 'moment';

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

  it('renders method.start_date_init when passed',  async () => {
    // const loc_value = createLocalVue();
    const wrapper = shallowMount(SalesOrderItemVue)
    await wrapper.setData({ start_date: null })
    await wrapper.vm.start_date_init()
    expect(wrapper.vm.start_date).not.toEqual(null)
  });

  it('renders method.end_date_init when passed',  async () => {
    // const loc_value = createLocalVue();
    const wrapper = shallowMount(SalesOrderItemVue)
    await wrapper.setData({ end_date: null })
    await wrapper.vm.end_date_init()
    expect(wrapper.vm.end_date).not.toEqual(null)
  });
})