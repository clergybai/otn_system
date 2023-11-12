<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-16 11:04:39
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-30 15:58:38
 * @FilePath: \hebei--vue\src\views\WDM-OTN\transmissionSystem\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="main">
    <div class="navigation">
      <div class="searchBox">
        <input
          type="text"
          placeholder="搜索省市或系统名称"
          v-model="menuArr.menuArrSearchVal"
          @keyup.enter="Search()"
        />
        <el-icon @click="Search()"><Search /></el-icon>
      </div>
      <el-scrollbar height="100%" v-loading.lock="navigationLoading">
        <template v-if="menuArr.menuArrTransitData.length > 0">
          <el-menu @select="selectItems" :unique-opened="true">
            <template
              v-for="(item, Itemindex) of menuArr.menuArrTransitData"
              :key="item.name + '-' + Itemindex"
            >
              <template v-if="Array.isArray(item.children) && item.children.length > 0">
                <el-sub-menu :index="item.name">
                  <template #title>{{ item.name }}</template>
                  <template
                    v-for="(children, ChilIndex) of item.children"
                    :key="children.name + '-' + ChilIndex"
                  >
                    <el-tooltip
                      class="box-item"
                      effect="customized"
                      :content="children.name"
                      placement="right"
                      :show-after="350"
                    >
                      <el-menu-item :index="children.name">{{
                        children.name
                      }}</el-menu-item>
                    </el-tooltip>
                  </template>
                </el-sub-menu>
              </template>
              <template v-else>
                <el-tooltip
                  class="box-item"
                  effect="customized"
                  :content="item.name"
                  placement="right"
                  :show-after="350"
                >
                  <el-menu-item :index="item.name">
                    {{ item.name }}
                  </el-menu-item>
                </el-tooltip>
              </template>
            </template>
          </el-menu>
        </template>
        <template v-else>
          <div class="dataEmpty">
            <svg
              t="1661509221350"
              class="icon"
              viewBox="0 0 1024 1024"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              p-id="4111"
              data-spm-anchor-id="a313x.7781069.0.i68"
              width="200"
              height="200"
            >
              <path
                d="M787.204195 852.226186h18.57855v11.49346h-18.57855z"
                fill="#C9C9C9"
                p-id="4112"
              ></path>
              <path
                d="M792.567418 857.972916c0 3.253937-2.486923 5.74673-5.744773 5.74673-3.259807 0-5.748687-2.490837-5.748687-5.74673 0-3.259807 2.486923-5.748687 5.748687-5.748687 3.255893 0.001957 5.744773 2.684547 5.744773 5.748687zM811.339678 857.972916c0 3.253937-2.490837 5.74673-5.748686 5.74673-3.25785 0-5.74673-2.490837-5.74673-5.74673 0-3.259807 2.486923-5.748687 5.74673-5.748687 3.25785 0.001957 5.748687 2.684547 5.748686 5.748687zM254.695392 852.226186h503.201849v11.49346H254.695392z"
                fill="#bfbfbf"
                p-id="4113"
                data-spm-anchor-id="a313x.7781069.0.i65"
                class=""
              ></path>
              <path
                d="M763.452217 857.972916c0 3.253937-2.48888 5.74673-5.74673 5.74673-3.25785 0-5.74673-2.490837-5.74673-5.74673 0-3.259807 2.486923-5.748687 5.74673-5.748687 3.255893 0.001957 5.74673 2.684547 5.74673 5.748687zM260.440166 857.972916c0 3.253937-2.48888 5.74673-5.74673 5.74673-3.255893 0-5.748687-2.490837-5.748687-5.74673 0-3.259807 2.490837-5.748687 5.748687-5.748687 3.06414 0.001957 5.74673 2.684547 5.74673 5.748687z"
                fill="#C9C9C9"
                p-id="4114"
              ></path>
              <path
                d="M474.209917 881.722937m-9.002623 0a9.002624 9.002624 0 1 0 18.005247 0 9.002624 9.002624 0 1 0-18.005247 0Z"
                fill="#bfbfbf"
                p-id="4115"
                data-spm-anchor-id="a313x.7781069.0.i67"
                class=""
              ></path>
              <path
                d="M351.235371 874.827643h96.733689v11.491504h-96.733689zM504.667391 874.827643h102.863926v11.491504h-102.863926z"
                fill="#bfbfbf"
                p-id="4116"
                data-spm-anchor-id="a313x.7781069.0.i66"
                class=""
              ></path>
              <path
                d="M356.600551 880.572417c0 3.25785-2.490837 5.74673-5.74673 5.74673s-5.748687-2.486923-5.748686-5.74673c0-3.253937 2.490837-5.74673 5.748686-5.74673 3.255893 0.001957 5.74673 2.68259 5.74673 5.74673zM453.907544 880.572417c0 3.25785-2.490837 5.74673-5.748687 5.74673-3.255893 0-5.748687-2.486923-5.748687-5.74673 0-3.253937 2.490837-5.74673 5.748687-5.74673 3.066097 0.001957 5.748687 2.68259 5.748687 5.74673zM510.030615 880.572417c0 3.25785-2.48888 5.74673-5.74673 5.74673-3.255893 0-5.748687-2.486923-5.748687-5.74673 0-3.253937 2.490837-5.74673 5.748687-5.74673 3.066097 0.001957 5.74673 2.68259 5.74673 5.74673zM613.084337 880.572417c0 3.25785-2.48888 5.74673-5.74673 5.74673-3.255893 0-5.748687-2.486923-5.748687-5.74673 0-3.253937 2.490837-5.74673 5.748687-5.74673 3.25785 0.001957 5.74673 2.68259 5.74673 5.74673z"
                fill="#C9C9C9"
                p-id="4117"
              ></path>
              <path
                d="M606.191 898.769417h93.665636v11.49346h-93.665636zM736.6361 898.769417h42.907744v11.49346h-42.907744z"
                fill="#bfbfbf"
                p-id="4118"
                data-spm-anchor-id="a313x.7781069.0.i70"
                class=""
              ></path>
              <path
                d="M611.935774 904.516147c0 3.25785-2.48888 5.74673-5.74673 5.74673-3.25785 0-5.748687-2.486923-5.748687-5.74673 0-3.253937 2.48888-5.748687 5.748687-5.748687 3.06414 0.001957 5.74673 2.684547 5.74673 5.748687zM785.863878 904.516147c0 3.25785-2.48888 5.74673-5.748687 5.74673-3.255893 0-5.74673-2.486923-5.74673-5.74673 0-3.253937 2.48888-5.748687 5.74673-5.748687 3.25785 0.001957 5.748687 2.684547 5.748687 5.748687zM710.201533 910.262877a10.127707 10.127707 0 0 1-1.72578-5.74673c0-5.55302 4.600123-10.151187 10.153143-10.151187s10.151187 4.598167 10.151187 10.151187a10.117924 10.117924 0 0 1-1.72578 5.74673h12.643981a19.433614 19.433614 0 0 0 0.573303-4.787963c0-11.683257-9.577884-21.26114-21.263097-21.261141-11.683257 0-21.259184 9.57984-21.259184 21.261141 0 1.534027 0.189797 3.259807 0.57526 4.787963h11.876967zM591.823197 904.516147c0 3.25785-2.486923 5.74673-5.748687 5.74673h-9.577884c-3.255893 0-5.74673-2.486923-5.74673-5.74673 0-3.253937 2.48888-5.748687 5.74673-5.748687h9.577884c3.066097 0.001957 5.748687 2.684547 5.748687 5.748687z"
                fill="#bfbfbf"
                p-id="4119"
                data-spm-anchor-id="a313x.7781069.0.i69"
                class=""
              ></path>
              <path
                d="M228.644332 226.049792c-10.340984 10.726447-27.393334 10.920157-38.115868 0.573303l-17.623697-17.048437c-10.726447-10.34294-10.920157-27.391377-0.57526-38.117824 10.34294-10.728404 27.393334-10.9182 38.115868-0.57526l17.623697 17.048437c10.728404 10.53665 10.920157 27.585087 0.57526 38.119781z"
                fill="#E9E8E8"
                p-id="4120"
              ></path>
              <path
                d="M467.889884 148.855377c0 0.765057-1.148563 1.53207-2.48888 1.53207h-25.859307c-1.342273 0-2.48888-0.767013-2.48888-1.53207V144.83247c0-0.765057 1.148563-1.53207 2.48888-1.53207h25.859307c1.342273 0 2.48888 0.767013 2.48888 1.53207v4.022907z"
                fill="#dbdbdb"
                p-id="4121"
                data-spm-anchor-id="a313x.7781069.0.i61"
                class=""
              ></path>
              <path
                d="M450.649694 162.264414c-0.767013 0-1.530113-1.15052-1.530114-2.492794V133.912313c0-1.33836 0.765057-2.48888 1.530114-2.48888h4.022906c0.76897 0 1.53207 1.15052 1.53207 2.48888v25.859307c0 1.342273-0.765057 2.492793-1.53207 2.492794h-4.022906z"
                fill="#dbdbdb"
                p-id="4122"
                data-spm-anchor-id="a313x.7781069.0.i60"
                class=""
              ></path>
              <path
                d="M608.104621 117.822643c-13.217284 0-23.753934 10.726447-23.753934 23.751977 0 13.027487 10.728404 23.753934 23.753934 23.753934 13.217284 0 23.751977-10.726447 23.751977-23.753934 0-13.02553-10.726447-23.751977-23.751977-23.751977z m-0.383507 35.053684c-6.130237 0-10.916244-4.979717-10.916244-10.9182s4.979717-10.920157 10.916244-10.920157c5.938483 0 10.9182 4.981673 10.9182 10.920157 0 5.938483-4.979717 10.9182-10.9182 10.9182z"
                fill="#E9E8E8"
                p-id="4123"
              ></path>
              <path
                d="M503.900378 332.551161m-15.324614 0a15.324614 15.324614 0 1 0 30.649228 0 15.324614 15.324614 0 1 0-30.649228 0Z"
                fill="#E9E8E8"
                p-id="4124"
              ></path>
              <path
                d="M284.002346 436.753447m-9.194376 0a9.194377 9.194377 0 1 0 18.388753 0 9.194377 9.194377 0 1 0-18.388753 0Z"
                fill="#dbdbdb"
                p-id="4125"
                data-spm-anchor-id="a313x.7781069.0.i64"
                class=""
              ></path>
              <path
                d="M883.17087 684.620072l-44.058264-40.416907c4.78992-22.411661 7.280757-45.780131 7.280757-69.534065 0-185.034144-149.984373-335.210271-335.214185-335.210271-46.547144 0-90.793249 9.577884-131.212113 26.624364l-38.884837-40.416908c-4.02095-4.21466-10.9182-4.404457-15.132861-0.189797-4.210747 4.02095-4.404457 10.916244-0.191753 15.130904l33.905121 35.053684c7.662307 10.534694 6.893337 25.094251-2.299084 34.861931-10.34294 10.920157-27.583131 11.301707-38.50133 0.767013l-6.703541-6.513743-39.078547-37.926071c-10.534694-10.151187-27.009827-9.76768-37.161014 0.573303-10.151187 10.534694-9.76768 27.009827 0.57526 37.162971l44.248061 42.905788a26.516747 26.516747 0 0 1-0.767014 34.861931c-9.959434 10.920157-26.816117 11.685214-37.54452 1.723823l-4.214661-3.831153-0.191753 0.189796-38.117824-34.86193c-16.473177-14.941107-41.757224-13.790587-56.890085 2.490836-14.941107 16.473177-13.790587 41.757224 2.490837 56.890085l53.250685 48.654474c-14.559557 37.544521-22.411661 78.149268-22.411661 120.67742 0 110.714073 53.634191 208.790035 136.19183 269.892823h397.849042a333.504058 333.504058 0 0 0 50.186545-45.588378l17.62174 16.091627c16.473177 14.93915 41.757224 13.790587 56.890085-2.490837s13.792544-41.759181-2.48888-56.888128l-25.284048-23.18063v-0.191754l-36.010494-32.946354c-7.662307-6.893337-8.239524-18.774217-1.15052-26.434567 7.08509-7.662307 18.77226-8.23561 26.432611-1.148563l27.20158 24.902497v-0.19371l26.624364 24.327237c9.96139 9.196334 25.667554 8.42932 34.861931-1.530113 8.626944-9.577884 8.051684-25.098164-2.10146-34.288628zM260.440166 566.435446c0 0.761143-1.15052 1.528157-2.48888 1.528157h-9.38613v9.38613c0 1.340317-0.76897 2.490837-1.53207 2.490837h-4.024864c-0.765057 0-1.53207-1.152477-1.53207-2.490837v-9.38613h-9.38613c-1.340317 0-2.48888-0.76897-2.48888-1.528157v-4.02682c0-0.765057 1.15052-1.53207 2.48888-1.53207h9.38613v-9.384173c0-1.342273 0.76897-2.492793 1.53207-2.492794h4.024864c0.765057 0 1.53207 1.152477 1.53207 2.492794v9.384173h9.38613c1.340317 0 2.48888 0.76897 2.48888 1.53207v4.02682z m23.372384-107.845599c-11.876967 0-21.646604-9.577884-21.646604-21.644647s9.577884-21.644647 21.646604-21.644647c11.873054 0 21.644647 9.577884 21.644647 21.644647s-9.771594 21.644647-21.644647 21.644647z m220.087828-98.647309c-15.51441 0-27.964681-12.45027-27.96468-27.96468s12.45027-27.964681 27.96468-27.964681c15.516367 0 27.966637 12.45027 27.966637 27.964681s-12.45027 27.964681-27.966637 27.96468z m208.983745 20.687837c0 0.765057-1.152477 1.53207-2.490837 1.53207h-9.38613v9.384174c0 1.342273-0.767013 2.490837-1.530113 2.490837h-4.024864c-0.767013 0-1.53207-1.15052-1.53207-2.490837v-9.384174h-9.38613c-1.342273 0-2.490837-0.767013-2.490837-1.53207v-3.831153c0-0.767013 1.15052-1.534027 2.490837-1.534027h9.38613v-9.384173c0-1.342273 0.767013-2.48888 1.53207-2.48888h4.024864c0.765057 0 1.530113 1.148563 1.530113 2.48888v9.384173h9.38613c1.340317 0 2.490837 0.767013 2.490837 1.534027v3.831153z"
                fill="#E9E8E8"
                p-id="4126"
              ></path>
              <path
                d="M562.798003 711.250306c0-43.799984 35.503717-79.301745 79.301745-79.301745 1.447933 0 2.88804 0.04109 4.316407 0.12327V501.689345l-86.198996-86.198996H419.23541c-14.749354 0-26.816117 12.06872-26.816118 26.816118v263.381036c0 14.747397 12.066764 26.816117 26.816118 26.816117h146.466286a79.315442 79.315442 0 0 1-2.903693-21.253314z"
                fill="#FFFFFF"
                p-id="4127"
              ></path>
              <path
                d="M441.649027 513.564355h110.714072a5.967833 5.967833 0 0 1 5.938484 5.94044 5.967833 5.967833 0 0 1-5.938484 5.936527h-110.714072a5.967833 5.967833 0 0 1-5.938484-5.936527 5.965877 5.965877 0 0 1 5.938484-5.94044zM441.649027 565.47668h161.09237a5.967833 5.967833 0 0 1 5.938484 5.936526 5.96979 5.96979 0 0 1-5.938484 5.936527h-161.09237a5.967833 5.967833 0 0 1-5.938484-5.936527 5.96392 5.96392 0 0 1 5.938484-5.936526zM435.710543 623.323574a5.96392 5.96392 0 0 1 5.938484-5.938483h161.09237a5.967833 5.967833 0 0 1 5.938484 5.938483 5.967833 5.967833 0 0 1-5.938484 5.93457h-161.09237a5.961963 5.961963 0 0 1-5.938484-5.93457z"
                fill="#FFFFFF"
                p-id="4128"
              ></path>
              <path
                d="M760.241327 799.126165l-45.126604-44.312631c19.801467-32.946354 15.17982-76.194558-13.438387-104.276639-33.449217-32.821127-87.464959-32.314351-120.286086 1.136823-32.823084 33.455087-32.314351 87.466915 1.136823 120.291956 28.616251 28.080124 71.944678 31.883884 104.507526 11.458241l44.568954 43.735414s8.66412-7.42555 16.441871-15.352007c7.781664-7.928414 12.195904-12.681157 12.195903-12.681157z m-71.737271-42.344224c-25.233174 25.718427-66.415138 26.111717-91.939856 0.870716-25.714514-25.233174-26.107804-66.417095-0.870716-91.939855s66.417095-26.105847 91.939855-0.870717c25.716471 25.045334 26.103891 66.227298 0.870717 91.939856z"
                fill="#4C64F2"
                p-id="4129"
                data-spm-anchor-id="a313x.7781069.0.i63"
                class=""
              ></path>
              <path
                d="M602.741397 565.47668h-161.09237a5.96392 5.96392 0 0 0-5.938484 5.936526 5.967833 5.967833 0 0 0 5.938484 5.936527h161.09237a5.96979 5.96979 0 0 0 5.938484-5.936527 5.967833 5.967833 0 0 0-5.938484-5.936526zM441.649027 525.251525h110.714072a5.96979 5.96979 0 0 0 5.938484-5.942397 5.965877 5.965877 0 0 0-5.938484-5.93457h-110.714072a5.96392 5.96392 0 0 0-5.938484 5.93457c0 3.449603 2.678677 5.942397 5.938484 5.942397zM602.741397 617.576844h-161.09237a5.967833 5.967833 0 0 0-5.938484 5.936527 5.965877 5.965877 0 0 0 5.938484 5.936527h161.09237a5.967833 5.967833 0 0 0 5.938484-5.936527 5.96979 5.96979 0 0 0-5.938484-5.936527zM587.035233 501.689345h59.382878l-86.198995-86.198996v59.380922c0 14.749354 12.064807 26.818074 26.816117 26.818074z"
                fill="#4C64F2"
                p-id="4130"
                data-spm-anchor-id="a313x.7781069.0.i62"
                class=""
              ></path>
            </svg>
            <span> 暂无数据... </span>
          </div>
        </template>
      </el-scrollbar>
    </div>
    <div class="content">
      <div id="container" v-loading.lock="canvasLoading">
        <div class="systemDetail" v-show="system_DetailsIsShow || systemAbnormal">
          <ul v-if="!systemAbnormal">
            <li>
              {{ system_Details.sys_name }}
            </li>
            <li>{{ system_Details.full_waves + " " }}<span>波道</span></li>
            <li><span>拓扑段长度:&nbsp;</span>{{ system_Details.fiber_lengtn }}</li>
            <li><span>系统隐患总数量:&nbsp;</span>{{ system_Details.risk_sum }}</li>
          </ul>
          <template v-else>
            <div class="systemAbnormal">资源数据异常!!!</div>
          </template>
        </div>
        <div class="zoomInOn">
          <button class="magnify" @click="zoomInOn(false)">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-dash"
              viewBox="0 0 16 16"
            >
              <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z" />
            </svg>
          </button>
          <button class="reduce" @click="zoomInOn(true)">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-plus"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- ROADM站详情 -->
  <Exmodal
    v-for="modalMainRoadmBoardDetail of modalMainRoadmBoardDetails"
    :key="modalMainRoadmBoardDetail.key"
    v-on:confirmModal="modalExit('ROADM::'+ modalMainRoadmBoardDetail.key)"
    :modalShow="modalMainRoadmBoardDetail.modalShow"
    :modalTitle="modalMainRoadmBoardDetail.modalTitle"
    :modalIsMark="modalMainRoadmBoardDetail.modalIsMark"
    :modalWidth="modalMainRoadmBoardDetail.modalWidth"
    :modalMinWidth="modalMainRoadmBoardDetail.modalMinWidth"
    :modalZIndex="modalMainRoadmBoardDetail.modalZIndex"
  >
    <div class="Content">
      <div class="modalMainRoadmBoardDetails">
        <span class="title">{{ modalMainRoadmBoardDetail.modalData.sub_name }}</span>
        <div class="graph">
          <div class="graphContent">
            <div class="graphTitle">
              {{ modalMainRoadmBoardDetail.modalData.manufactor_type_model }}
            </div>
            <div class="contentMain">
              <div class="mainLeft">
                <div class="mainRouting" :act-stand="modalMainRoadmBoardDetail.mainAct_stand">
                  <span class="SubName">{{
                    modalMainRoadmBoardDetail.modalData.sub_nameArr[0].subName
                  }}</span>
                  <div class="mainRoutingOne">
                    <label class="slot-info-one">{{ getSlotInfo(modalMainRoadmBoardDetail.modalData.mainFingerprint[0].oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[0].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[0]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[0].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[0]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[0]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="mainRoutingTwo">
                    <label class="slot-info-two">{{ getSlotInfo(modalMainRoadmBoardDetail.modalData.mainFingerprint[2]
                    .oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[2].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[2]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[2].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[2]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[2]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
                <div class="viceRouting" :act-stand="alterAct_stand">
                  <span class="SubName">{{
                    modalMainRoadmBoardDetail.modalData.sub_nameArr[2].subName
                  }}</span>
                  <div class="viceRoutingOne">
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[4].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[4]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[4].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[4]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[4]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="viceRoutingTwo">
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[6].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[6]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[6].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[6]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[6]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
              </div>
              <div class="pillars">
                <span>ROADM</span>
              </div>
              <div class="mainRight">
                <div class="mainRouting" :act-stand="mainAct_stand">
                  <span class="SubName">{{
                    modalMainRoadmBoardDetail.modalData.sub_nameArr[1].subName
                  }}</span>
                  <div class="mainRoutingOne">
                    <label class="slot-info-one">{{ getSlotInfo(modalMainRoadmBoardDetail.modalData.mainFingerprint[1].oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[1].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[1]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[1].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[1]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[1]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="mainRoutingTwo">
                    <label class="slot-info-two">{{ getSlotInfo(modalMainRoadmBoardDetail.modalData.mainFingerprint[3]
                    .oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[3].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[3]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[3].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[3]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[3]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
                <div class="viceRouting" :act-stand="modalMainRoadmBoardDetail.alterAct_stand">
                  <span class="SubName">{{
                    modalMainRoadmBoardDetail.modalData.sub_nameArr[3].subName
                  }}</span>
                  <div class="viceRoutingOne">
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[5].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[5]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[5].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[5]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[5]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="viceRoutingTwo">
                    <hr />
                    <template
                      v-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[7].isHigh ==
                        2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[7]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainRoadmBoardDetail.modalData.mainFingerprint[7].isHigh ==
                        1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[7]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainRoadmBoardDetail.modalData.mainFingerprint[7]
                              .oa_fingerprintName, modalMainRoadmBoardDetail
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="prompt">*注意：本图复用段左右方向可能与ToPo图方向存在不一致</div>
    </div>
  </Exmodal>
  <!-- OLP站详情 -->
  <Modal
    v-on:confirmModal="modalExit('OLP')"
    :modalShow="modalMainOlpBoardDetails.modalShow"
    :modalTitle="modalMainOlpBoardDetails.modalTitle"
    :modalIsMark="modalMainOlpBoardDetails.modalIsMark"
    :modalWidth="modalMainOlpBoardDetails.modalWidth"
    :modalMinWidth="modalMainOlpBoardDetails.modalMinWidth"
    :modalZIndex="modalMainOlpBoardDetails.modalZIndex"
  >
    <div class="Content">
      <div class="modalMainOlpBoardDetails">
        <span class="title">
          {{ modalMainOlpBoardDetails.modalData.sub_name }}
        </span>
        <div class="graph">
          <div class="graphContent">
            <div class="graphTitle">
              {{ modalMainOlpBoardDetails.modalData.manufactor_type_model }}
            </div>
            <div class="contentMain">
              <div class="mainLeft">
                <div class="pillars">
                  <span>OLP</span>
                </div>
                <div class="mainRouting">
                  <span class="SubName">{{
                    modalMainOlpBoardDetails.modalData.sub_nameArr[0].subName
                  }}</span>
                  <div class="mainRoutingOne">
                    <label class="slot-info-one">{{ getSlotInfo(modalMainOlpBoardDetails.modalData.mainFingerprint[0].oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[0].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[0]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[0].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[0]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[0]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="mainRoutingTwo">
                    <label class="slot-info-two">{{ getSlotInfo(modalMainOlpBoardDetails.modalData.mainFingerprint[2]
                    .oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[2].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[2]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[2].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[2]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[2]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
                <div class="viceRouting">
                  <span class="SubName">{{
                    modalMainOlpBoardDetails.modalData.sub_nameArr[2].subName
                  }}</span>
                  <div class="viceRoutingOne">
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[4].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[4]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[4].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[4]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[4]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="viceRoutingTwo">
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[6].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[6]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[6].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[6]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[6]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
              </div>
              <div class="mainRight">
                <div class="pillars">
                  <span>OLP</span>
                </div>
                <div class="mainRouting">
                  <span class="SubName">{{
                    modalMainOlpBoardDetails.modalData.sub_nameArr[1].subName
                  }}</span>
                  <div class="mainRoutingOne">
                    <label class="slot-info-one">{{ getSlotInfo(modalMainOlpBoardDetails.modalData.mainFingerprint[1].oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[1].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[1]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[1].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[1]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[1]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="mainRoutingTwo">
                    <label class="slot-info-two">{{ getSlotInfo(modalMainOlpBoardDetails.modalData.mainFingerprint[3]
                    .oa_fingerprintName) }}</label>
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[3].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[3]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[3].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[3]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[3]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
                <div class="viceRouting">
                  <span class="SubName">{{
                    modalMainOlpBoardDetails.modalData.sub_nameArr[3].subName
                  }}</span>
                  <div class="viceRoutingOne">
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[5].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[5]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[5].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[5]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_right.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[5]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                  <div class="viceRoutingTwo">
                    <hr />
                    <template
                      v-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[7].isHigh == 2
                      "
                    >
                      <img
                        src="../../../assets/oa_card_red_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[7]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template
                      v-else-if="
                        modalMainOlpBoardDetails.modalData.mainFingerprint[7].isHigh == 1
                      "
                    >
                      <img
                        src="../../../assets/oa_card_yellow_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[7]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                    <template v-else>
                      <img
                        src="../../../assets/oa_card_blue_left.png"
                        @click="
                          selectOaContent(
                            modalMainOlpBoardDetails.modalData.mainFingerprint[7]
                              .oa_fingerprintName
                          )
                        "
                      />
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="prompt">*注意：本图复用段左右方向可能与ToPo图方向存在不一致</div>
    </div>
  </Modal>
  <!--MUN2详情 -->
  <Modal
    @keydown.esc="modalExit('MUX2')"
    v-on:confirmModal="modalExit('MUX2')"
    :modalShow="modalMainBoardDetails.modalShow"
    :modalTitle="modalMainBoardDetails.modalTitle"
    :modalIsMark="modalMainBoardDetails.modalIsMark"
    :modalWidth="modalMainBoardDetails.modalWidth"
    :modalMinWidth="modalMainBoardDetails.modalMinWidth"
    :modalZIndex="modalMainBoardDetails.modalZIndex"
  >
    <div class="Content">
      <div class="modalMainBoardDetails">
        <span class="title">
          {{ modalMainBoardDetails.modalData.sub_name }}
        </span>
        <div class="graph">
          <div class="graphContent">
            <div class="graphTitle">
              {{ modalMainBoardDetails.modalData.manufactor_type_model }}
            </div>
            <div class="contentMain">
              <div class="mainLeft">
                <span class="SubName">
                  {{ modalMainBoardDetails.modalData.sub_nameArr[0].subName }}</span
                >
                <div class="pillars">
                  <span>MUX</span>
                </div>
                <div class="mainRoutingOne">
                  <label class="slot-info-one">{{ getSlotInfo(modalMainBoardDetails.modalData.mainFingerprint[0].oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[0].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[0]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[0].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[0]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[0]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
                <div class="mainRoutingTwo">
                  <label class="slot-info-two">{{ getSlotInfo(modalMainBoardDetails.modalData.mainFingerprint[1]
                    .oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[1].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[1]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[1].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[1]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[1]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
              </div>
              <div class="mainRight">
                <span class="SubName">{{
                  modalMainBoardDetails.modalData.sub_nameArr[1].subName
                }}</span>
                <div class="pillars">
                  <span>MUX</span>
                </div>
                <div class="mainRoutingOne">
                  <label class="slot-info-one">{{ getSlotInfo(modalMainBoardDetails.modalData.mainFingerprint[2].oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[2].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[2]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[2].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[2]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[2]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
                <div class="mainRoutingTwo">
                  <label class="slot-info-two">{{ getSlotInfo(modalMainBoardDetails.modalData.mainFingerprint[3]
                    .oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[3].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[3]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[3].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[3]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[3]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
              </div>
            </div>
            <div class="contentStandby">
              <div class="standbyLeft">
                <span class="SubName">{{
                  modalMainBoardDetails.modalData.sub_nameArr[2].subName
                }}</span>
                <div class="pillars">
                  <span>MUX</span>
                </div>
                <div class="standbyRoutingOne">
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[4].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[4]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[4].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[4]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[4]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
                <div class="standbyRoutingTwo">
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[5].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[5]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[5].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[5]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[5]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
              </div>
              <div class="standbyRight">
                <span class="SubName">{{
                  modalMainBoardDetails.modalData.sub_nameArr[3].subName
                }}</span>
                <div class="pillars">
                  <span>MUX</span>
                </div>
                <div class="standbyRoutingOne">
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[6].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[6]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[6].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[6]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_right.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[6]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
                <div class="standbyRoutingTwo">
                  <hr />
                  <template
                    v-if="modalMainBoardDetails.modalData.mainFingerprint[7].isHigh == 2"
                  >
                    <img
                      src="../../../assets/oa_card_red_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[7]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainBoardDetails.modalData.mainFingerprint[7].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[7]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_left.png"
                      @click="
                        selectOaContent(
                          modalMainBoardDetails.modalData.mainFingerprint[7]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="prompt">*注意：本图复用段左右方向可能与ToPo图方向存在不一致</div>
    </div>
  </Modal>
  <!--MUX详情 -->
  <Exmodal
    v-for="modalMainMuxBoardDetail of modalMainMuxBoardDetails"
    :key="modalMainMuxBoardDetail.key"
    v-on:confirmModal="modalExit('MUX::'+ modalMainMuxBoardDetail.key)"
    :modalShow="modalMainMuxBoardDetail.modalShow"
    :modalTitle="modalMainMuxBoardDetail.modalTitle"
    :modalIsMark="modalMainMuxBoardDetail.modalIsMark"
    :modalWidth="modalMainMuxBoardDetail.modalWidth"
    :modalMinWidth="modalMainMuxBoardDetail.modalMinWidth"
    :modalZIndex="modalMainMuxBoardDetail.modalZIndex"
  >
    <div class="Content">
      <div class="modalMainMuxBoardDetails">
        <span class="title">
          {{ modalMainMuxBoardDetail.modalData.sub_name }}
        </span>
        <div class="graph">
          <div class="graphContent">
            <div class="graphTitle">
              {{ modalMainMuxBoardDetail.modalData.manufactor_type_model }}
            </div>
            <div class="contentMain">
              <div class="mainLeft" :act-stand="modalMainMuxBoardDetail.act_standArr[0]">
                <span class="SubName">
                  {{ modalMainMuxBoardDetail.modalData.sub_nameArr[0].subName }}
                </span>
                <div class="pillars">
                  <span>{{ modalMainMuxBoardDetail.title }}</span>
                </div>
                <div class="mainRoutingOne">
                  <label class="slot-info-one">{{ getSlotInfo(modalMainMuxBoardDetail.modalData.mainFingerprint[0].oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[0].isHigh == 2
                    "
                  >
                    <img
                      src="../../../assets/oa_card_red_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[0]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[0].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[0]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[0]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                </div>
                <div class="mainRoutingTwo">
                  <label class="slot-info-two">{{ getSlotInfo(modalMainMuxBoardDetail.modalData.mainFingerprint[2]
                    .oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[2].isHigh == 2
                    "
                  >
                    <img
                      src="../../../assets/oa_card_red_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[2]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[2].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[2]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[2]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                </div>
              </div>
              <div class="mainRight" :act-stand="modalMainMuxBoardDetail.act_standArr[1]">
                <span class="SubName">
                  {{ modalMainMuxBoardDetail.modalData.sub_nameArr[1].subName }}
                </span>
                <div class="pillars">
                  <span>{{ modalMainMuxBoardDetail.title }}</span>
                </div>
                <div class="mainRoutingOne">
                  <label class="slot-info-one">{{ getSlotInfo(modalMainMuxBoardDetail.modalData.mainFingerprint[1].oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[1].isHigh == 2
                    "
                  >
                    <img
                      src="../../../assets/oa_card_red_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[1]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[1].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[1]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[1]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                </div>
                <div class="mainRoutingTwo">
                  <label class="slot-info-two">{{ getSlotInfo(modalMainMuxBoardDetail.modalData.mainFingerprint[3]
                    .oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[3].isHigh == 2
                    "
                  >
                    <img
                      src="../../../assets/oa_card_red_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[3]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainMuxBoardDetail.modalData.mainFingerprint[3].isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[3]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxBoardDetail.modalData.mainFingerprint[3]
                            .oa_fingerprintName, modalMainMuxBoardDetail
                        )
                      "
                    />
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="prompt">*注意：本图复用段左右方向可能与ToPo图方向存在不一致</div>
    </div>
  </Exmodal>
  <!-- MUX\ROADM单向 -->
  <Modal
    v-on:confirmModal="modalExit('MUX/ROADM')"
    :modalShow="modalMainMuxSingleBoardDetails.modalShow"
    :modalTitle="modalMainMuxSingleBoardDetails.modalTitle"
    :modalIsMark="modalMainMuxSingleBoardDetails.modalIsMark"
    :modalWidth="modalMainMuxSingleBoardDetails.modalWidth"
    :modalMinWidth="modalMainMuxSingleBoardDetails.modalMinWidth"
    :modalZIndex="modalMainMuxSingleBoardDetails.modalZIndex"
  >
    <div class="Content">
      <div class="modalMainMuxSingleBoardDetails">
        <span class="title">
          {{ modalMainMuxSingleBoardDetails.modalData.sub_name }}
        </span>
        <div class="graph">
          <div class="graphContent">
            <div class="graphTitle">
              {{ modalMainMuxSingleBoardDetails.modalData.manufactor_type_model }}
            </div>
            <div class="contentMain">
              <div class="mainRight">
                <span class="SubName">
                  {{ modalMainMuxSingleBoardDetails.modalData.sub_nameArr[0].subName }}
                </span>
                <div class="pillars">
                  <span>{{ modalMainMuxSingleBoardDetails.title }}</span>
                </div>
                <div class="mainRoutingOne">
                  <label class="slot-info-one">{{ getSlotInfo(modalMainMuxSingleBoardDetails.modalData.mainFingerprint[1].oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="
                      modalMainMuxSingleBoardDetails.modalData.mainFingerprint[1]
                        .isHigh == 2
                    "
                  >
                    <img
                      src="../../../assets/oa_card_red_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxSingleBoardDetails.modalData.mainFingerprint[1]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainMuxSingleBoardDetails.modalData.mainFingerprint[1]
                        .isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxSingleBoardDetails.modalData.mainFingerprint[1]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_right.png"
                      @click="
                        selectOaContent(
                          modalMainMuxSingleBoardDetails.modalData.mainFingerprint[1]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
                <div class="mainRoutingTwo">
                  <label class="slot-info-two">{{ getSlotInfo(modalMainMuxSingleBoardDetails.modalData.mainFingerprint[0]
                    .oa_fingerprintName) }}</label>
                  <hr />
                  <template
                    v-if="
                      modalMainMuxSingleBoardDetails.modalData.mainFingerprint[0]
                        .isHigh == 2
                    "
                  >
                    <img
                      src="../../../assets/oa_card_red_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxSingleBoardDetails.modalData.mainFingerprint[0]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template
                    v-else-if="
                      modalMainMuxSingleBoardDetails.modalData.mainFingerprint[0]
                        .isHigh == 1
                    "
                  >
                    <img
                      src="../../../assets/oa_card_yellow_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxSingleBoardDetails.modalData.mainFingerprint[0]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                  <template v-else>
                    <img
                      src="../../../assets/oa_card_blue_left.png"
                      @click="
                        selectOaContent(
                          modalMainMuxSingleBoardDetails.modalData.mainFingerprint[0]
                            .oa_fingerprintName
                        )
                      "
                    />
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="prompt">*注意：本图复用段左右方向可能与ToPo图方向存在不一致</div>
    </div>
  </Modal>
  <!-- OA点击详情 -->
  <Exmodal
    v-for="modalLightLetStandBoardCardDetail of modalLightLetStandBoardCardDetails"
    :key="modalLightLetStandBoardCardDetail.key"
    @keydown.esc="modalExit('OA::' + modalLightLetStandBoardCardDetail.key)"
    v-on:confirmModal="modalExit('OA::' + modalLightLetStandBoardCardDetail.key)"
    :modalShow="modalLightLetStandBoardCardDetail.modalShow"
    :modalTitle="modalLightLetStandBoardCardDetail.modalTitle"
    :modalIsMark="modalLightLetStandBoardCardDetail.modalIsMark"
    :modalWidth="modalLightLetStandBoardCardDetail.modalWidth"
    :modalMinWidth="modalLightLetStandBoardCardDetail.modalMinWidth"
    :modalZIndex="modalLightLetStandBoardCardDetail.modalZIndex"
  >
    <div :class="[modalLightLetStandBoardCardDetail.modalData.pre_position_Voa == true ? 'modalLightLetStandBoardCardBeforeDetails':'modalLightLetStandBoardCardAfterDetails']">
      <div class="topo">
        <div class="boardCard">
          <div class="cardIN">IN</div>
          <div class="cardExternalVOA">
            <span>外部VOA</span>
          </div>
          <div v-if="modalLightLetStandBoardCardDetail.modalData.pre_position_Voa" class="cardVOA">
            <span>VOA</span>
          </div>
          <div class="img">
            <img src="../../../assets/triangle-right.png" alt="" />
          </div>
          <div v-if="!modalLightLetStandBoardCardDetail.modalData.pre_position_Voa" class="cardVOA">
            <span>VOA</span>
          </div>
          <div class="cardOUT">OUT</div>
        </div>
      </div>
      <div class="table">
        <div class="tableOne">
          <ul>
            <li>
              <div class="Line"></div>
              <div class="title">入局输入光功率</div>
              <div class="value">
                {{
                  modalLightLetStandBoardCardDetail.modalData.ne_incoming_power
                }}dBm
              </div>
            </li>
            <li>
              <div class="Line"></div>
              <div class="title">外部可调光衰设置值</div>
              <div class="value">
                {{ modalLightLetStandBoardCardDetail.modalData.outside_voa }}dB
              </div>
            </li>
            <li>
              <div class="Line"></div>
              <div class="title">内部可调光衰设置值</div>
              <div class="value">
                {{ modalLightLetStandBoardCardDetail.modalData.inside_voa }}dB
              </div>
            </li>
            <li
              :style="{
                border: CheckState(
                  modalLightLetStandBoardCardDetail.modalData.ishigh
                    .input_power_input_stand_power
                ),
              }"
            >
              <div class="Line"></div>
              <div class="titleGroup">
                <div class="titleOne">光放实际输入功率</div>
                <div class="titleTwo">输入标准功率</div>
              </div>
              <div class="valueGroup">
                <div class="valueOne">
                  {{ modalLightLetStandBoardCardDetail.modalData.input_power }}dBm
                </div>
                <div class="valueTwo">
                  {{
                    modalLightLetStandBoardCardDetail.modalData.input_stand_power
                  }}dBm
                </div>
              </div>
            </li>
            <li
              :style="{
                border: CheckState(
                  modalLightLetStandBoardCardDetail.modalData.ishigh
                    .stand_gain_min_stand_gain_max
                ),
              }"
            >
              <div class="Line"></div>
              <div class="titleGroup">
                <div class="titleOne">实际增益</div>
                <div class="titleTwo">理论增益</div>
              </div>
              <div class="valueGroup">
                <div class="valueOne">
                  {{ modalLightLetStandBoardCardDetail.modalData.gain }}dB
                </div>
                <div class="valueTwo">
                  {{
                    modalLightLetStandBoardCardDetail.modalData.stand_gain_min
                  }}~{{
                    modalLightLetStandBoardCardDetail.modalData.stand_gain_max
                  }}dB
                </div>
              </div>
            </li>
            <li
              :style="{
                border: CheckState(
                  modalLightLetStandBoardCardDetail.modalData.ishigh
                    .output_power_output_stand_power
                ),
              }"
            >
              <div class="Line"></div>
              <div class="titleGroup">
                <div class="titleOne">光放实际输出功率</div>
                <div class="titleTwo">输出标准功率</div>
              </div>
              <div class="valueGroup">
                <div class="valueOne">
                  {{ modalLightLetStandBoardCardDetail.modalData.output_power }}dBm
                </div>
                <div class="valueTwo">
                  {{
                    modalLightLetStandBoardCardDetail.modalData.output_stand_power
                  }}dBm
                </div>
              </div>
            </li>
            <li v-if="!modalLightLetStandBoardCardDetail.modalData.pre_position_Voa">
              <div class="Line"></div>
              <div class="title">出局输出光功率</div>
              <div class="value">
                {{ modalLightLetStandBoardCardDetail.modalData.ne_outing_power }}dB
              </div>
            </li>
          </ul>
        </div>
        <div class="tableTwo">
          <div class="tableData">
            <div class="tableDataLine"></div>
            <div class="oaBoardType">
              <span class="dataTitle">OA板卡型号</span>
              <span class="dataValue">{{
                modalLightLetStandBoardCardDetail.modalData.brd_type
              }}</span>
            </div>
            <div class="slot">
              <span class="dataTitle">子架/槽位</span>
              <span class="dataValue"
                >{{ modalLightLetStandBoardCardDetail.modalData.shelf_id }}/{{
                  modalLightLetStandBoardCardDetail.modalData.slot_id
                }}</span
              >
            </div>
            <div class="channelNumber">
              <span class="dataTitle">波道数/复用段</span>
              <span class="dataValue"
                >{{ modalLightLetStandBoardCardDetail.modalData.wavs }}/{{
                  modalLightLetStandBoardCardDetail.modalData.oms
                }}</span
              >
            </div>
            <div class="troubleCount">
              <span class="dataTitle">光功率隐患数量</span>
              <span class="dataValue">{{
                modalLightLetStandBoardCardDetail.modalData.oa_risk_num
              }}</span>
            </div>
            <div class="direction">
              <div class="titleGroup">
                <div class="mainGroup">方向</div>
                <div class="viceGroup">
                  <span class="viceClosed">收</span>
                  <span class="viceHair">发</span>
                </div>
              </div>
              <div class="valueGroup">
                <div class="valueClosed">
                  {{
                    modalLightLetStandBoardCardDetail.modalData.in_ne_subname == ""
                      ? "内部"
                      : modalLightLetStandBoardCardDetail.modalData.in_ne_subname
                  }}
                </div>
                <div class="valueHair">
                  {{
                    modalLightLetStandBoardCardDetail.modalData.out_ne_subname == ""
                      ? "内部"
                      : modalLightLetStandBoardCardDetail.modalData.out_ne_subname
                  }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Exmodal>
  <!-- OLA点击详情 -->
  <Modal
    v-on:confirmModal="modalExit('OLA')"
    :modalShow="modalLightLetStandDetails.modalShow"
    :modalTitle="modalLightLetStandDetails.modalTitle"
    :modalIsMark="modalLightLetStandDetails.modalIsMark"
    :modalWidth="modalLightLetStandDetails.modalWidth"
    :modalMinWidth="modalLightLetStandDetails.modalMinWidth"
    :modalZIndex="modalLightLetStandDetails.modalZIndex"
  >
    <div class="Content">
      <div class="modalLightLetStandDetails">
        <span class="title">
          {{ modalLightLetStandDetails.modalData.sub_name }}
        </span>
        <div class="vice">
          <span class="SubName">{{
            modalLightLetStandDetails.modalData.source_sub_name
          }}</span>
          <span class="SubName">{{
            modalLightLetStandDetails.modalData.target_sub_name
          }}</span>
          <div class="viceRoutingOne">
            <hr />
            <div
              class="oa_fingerprint"
              v-for="item of modalLightLetStandDetails.modalData.source_oa_fingerprintArr"
              :key="item.oa_fingerprintName"
            >
              <template v-if="item.isHigh == 2">
                <label class="ola-slot-info-one">{{ getSlotInfo(item.oa_fingerprintName) }}</label>
                <img
                  src="../../../assets/oa_card_red_right.png"
                  @click="selectOaContent(item.oa_fingerprintName)"
                />
              </template>
              <template v-else-if="item.isHigh == 1">
                <label class="ola-slot-info-one">{{ getSlotInfo(item.oa_fingerprintName) }}</label>
                <img
                  src="../../../assets/oa_card_yellow_right.png"
                  @click="selectOaContent(item.oa_fingerprintName)"
                />
              </template>
              <template v-else>
                <label class="ola-slot-info-one">{{ getSlotInfo(item.oa_fingerprintName) }}</label>
                <img
                  src="../../../assets/oa_card_blue_right.png"
                  @click="selectOaContent(item.oa_fingerprintName)"
                />
              </template>
            </div>
          </div>
          <div class="viceRoutingTwo">
            <hr />
            <div
              class="oa_fingerprint"
              v-for="item of modalLightLetStandDetails.modalData.target_oa_fingerprintArr"
              :key="item.oa_fingerprintName"
            >
              <template v-if="item.isHigh == 2">
                <label class="ola-slot-info-three">{{ getSlotInfo(item.oa_fingerprintName) }}</label>
                <img
                  src="../../../assets/oa_card_red_left.png"
                  @click="selectOaContent(item.oa_fingerprintName)"
                />
              </template>
              <template v-else-if="item.isHigh == 1">
                <label class="ola-slot-info-three">{{ getSlotInfo(item.oa_fingerprintName) }}</label>
                <img
                  src="../../../assets/oa_card_yellow_left.png"
                  @click="selectOaContent(item.oa_fingerprintName)"
                />
              </template>
              <template v-else>
                <label class="ola-slot-info-three">{{ getSlotInfo(item.oa_fingerprintName) }}</label>
                <img
                  src="../../../assets/oa_card_blue_left.png"
                  @click="selectOaContent(item.oa_fingerprintName)"
                />
              </template>
            </div>
          </div>
        </div>
      </div>
      <div class="prompt">*注意：本图复用段左右方向可能与ToPo图方向存在不一致</div>
    </div>
  </Modal>
  <!-- 光缆点击详情 -->
  <Modal
    v-on:confirmModal="modalExit('CABLE')"
    :modalShow="modalCableDetails.modalShow"
    :modalTitle="modalCableDetails.modalTitle"
    :modalIsMark="modalCableDetails.modalIsMark"
    :modalWidth="modalCableDetails.modalWidth"
    :modalMinWidth="modalCableDetails.modalMinWidth"
    :modalZIndex="modalCableDetails.modalZIndex"
  >
    <div class="modalCableDetails">
      <div class="opticalCableSignalling">
        <span class="subName">{{ modalCableDetails.modalData.fiber_name }}</span>
        <div class="opticalCableReceive">
          <div class="send">
            <span class="sendTitle">
              {{ modalCableDetails.modalData.source_sub_name }}
            </span>
            <span class="sendVal"></span>
          </div>
          <div class="sendData">
            <div class="longLeather">
              <span class="longLeatherTitle">皮长:</span>
              <span class="longLeatherVal">
                {{ computedKM(modalCableDetails.modalData.fiber_length) }}
              </span>
            </div>
            <div class="loss">
              <div class="lossTitle">
                <span>理论损耗:</span>
                <span>{{ modalCableDetails.modalData.stand_fiber_loss }}dB</span>
              </div>
              <div class="lossVal">
                <span>实际损耗:</span>
                <span>{{ modalCableDetails.modalData.source_out_fiber_loss }}dB</span>
              </div>
            </div>
          </div>
          <div class="receive">
            <span class="sendVal"></span>
            <span class="sendTitle">
              {{ modalCableDetails.modalData.target_sub_name }}
            </span>
          </div>
        </div>
        <div class="fiberOrientation">
          <div class="contentIn">
            <span class="slot"
              >槽位:{{ modalCableDetails.modalData.source_out_shelf_slot }}</span
            >
            <span class="output"
              >输出光功率:{{ modalCableDetails.modalData.source_outing_power }}dBm</span
            >
          </div>
          <hr />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-caret-right-fill"
            viewBox="0 0 16 16"
          >
            <path
              d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"
            />
          </svg>
          <img src="../../../assets/triangle-right.png" alt="" />
          <img src="../../../assets/triangle-right.png" alt="" />
          <div class="contentOut">
            <span class="slot"
              >槽位:{{ modalCableDetails.modalData.target_in_shelf_slot }}</span
            >
            <span class="output"
              >入局光功率:{{ modalCableDetails.modalData.target_incoming_power }}dBm</span
            >
          </div>
        </div>
      </div>
      <div
        class="opticalCableTitle"
        v-if="modalCableDetails.modalData.is_risk == ('high' || 'higher')"
      >
        光缆收发损耗偏差隐患
      </div>
      <div class="opticalCableReception">
        <div class="fiberOpticCableToSend">
          <div class="send">
            <span class="sendVal"></span>
          </div>
          <div class="sendData">
            <div class="longLeather">
              <span class="longLeatherTitle">皮长:</span>
              <span class="longLeatherVal">
                {{ computedKM(modalCableDetails.modalData.fiber_length) }}
              </span>
            </div>
            <div class="loss">
              <div class="lossTitle">
                <span>理论损耗:</span>
                <span>{{ modalCableDetails.modalData.stand_fiber_loss }}dB</span>
              </div>
              <div class="lossVal">
                <span>实际损耗:</span>
                <span>{{ modalCableDetails.modalData.source_in_fiber_loss }}dB</span>
              </div>
            </div>
          </div>
          <div class="receive">
            <span class="sendVal"></span>
          </div>
        </div>
        <div class="fiberOrientation">
          <div class="contentIn">
            <span class="slot"
              >槽位:{{ modalCableDetails.modalData.source_in_shelf_slot }}</span
            >
            <span class="output"
              >入局光功率:{{ modalCableDetails.modalData.source_incoming_power }}dBm</span
            >
          </div>
          <hr />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-caret-right-fill"
            viewBox="0 0 16 16"
          >
            <path
              d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"
            />
          </svg>
          <img src="../../../assets/triangle-left.png" alt="" />
          <img src="../../../assets/triangle-left.png" alt="" />
          <div class="contentOut">
            <span class="slot"
              >槽位:{{ modalCableDetails.modalData.target_out_shelf_slot }}</span
            >
            <span class="output"
              >输出光功率:{{ modalCableDetails.modalData.target_outing_power }}dBm</span
            >
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script>
import G6 from "@antv/g6";
import icon_node from "../../../assets/Node.png";
import icon_amp from "../../../assets/Amplifier.png";
import icon_node_red from "../../../assets/Node_red.jpg";
import icon_node_yellow from "../../../assets/Node_yellow.jpg";
import icon_amp_red from "../../../assets/Amplifier_red.jpg";
import icon_amp_yellow from "../../../assets/Amplifier_yellow.jpg";
import Modal from "../../Component/modal.vue";
import Exmodal from "../../Component/exmodal.vue";
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { getUserName, getIs_Authen } from "@/config/UserInfomation";
import * as _ from "lodash";
import {
  getMenu,
  getDraw,
  getMain,
  getOa,
  getOla,
  getFiber,
  setPosition,
} from "@/api/WDM-OTN/http";
import { forEach } from 'lodash';

export default {
  data() {
    return {
      visible: ref(false),
      menuBtnVal: false,
      canvasLoading: false,
      navigationLoading: false,
      system_DetailsIsShow: false,
      systemAbnormal: false,
      defaultActive: {
        perms: true,
        sys_name: "",
        code: "",
        user_name: "",
      },
      act_standArr: ["主路由", "备路由"],
      mainAct_stand: "主路由",
      alterAct_stand: "备路由",
      ratioLocal: 0.3,
      graphLocal: null,
      system_Details: {
        sys_name: "",
        full_waves: "",
        fiber_lengtn: "",
        risk_sum: "",
      },
      modalMainRoadmBoardDetails: [
        {
          key: "",
          modalData: {}, // 弹框内数据
          modalIsMark: false, // 是否展示蒙层
          modalWidth: "1100px", // 弹出层宽度'
          modalMinWidth: "600px", // 最小宽度
          modalShow: false, // modal显示标识
          modalZIndex: "5", // 弹框层级
          mainAct_stand: "",
          alterAct_stand: "",
        },
        {
          key: "",
          modalData: {}, // 弹框内数据
          modalIsMark: false, // 是否展示蒙层
          modalWidth: "1100px", // 弹出层宽度'
          modalMinWidth: "600px", // 最小宽度
          modalShow: false, // modal显示标识
          modalZIndex: "5", // 弹框层级
        },
      ],
      modalMainOlpBoardDetails: {
        modalData: {}, // 弹框内数据
        modalIsMark: false, // 是否展示蒙层
        modalWidth: "1100px", // 弹出层宽度'
        modalMinWidth: "600px", // 最小宽度
        modalShow: false, // modal显示标识
        modalZIndex: "5", // 弹框层级
      },
      modalMainBoardDetails: {
        modalData: {}, // 弹框内数据
        modalIsMark: false, // 是否展示蒙层
        modalWidth: "1100px", // 弹出层宽度'
        modalMinWidth: "600px", // 最小宽度
        modalShow: false, // modal显示标识
        modalZIndex: "5", // 弹框层级
      },
      modalMainMuxBoardDetails: [
        {
          key: "",
          title: "",
          modalData: {}, // 弹框内数据
          modalIsMark: false, // 是否展示蒙层
          modalWidth: "1100px", // 弹出层宽度'
          modalMinWidth: "600px", // 最小宽度
          modalShow: false, // modal显示标识
          modalZIndex: "5", // 弹框层级
          act_standArr: [],
          child: null,
        },
        {
          key: "",
          title: "",
          modalData: {}, // 弹框内数据
          modalIsMark: false, // 是否展示蒙层
          modalWidth: "1100px", // 弹出层宽度'
          modalMinWidth: "600px", // 最小宽度
          modalShow: false, // modal显示标识
          modalZIndex: "5", // 弹框层级
          act_standArr: [],
          child: null,
        }
      ],
      modalMainMuxSingleBoardDetails: {
        title: "",
        modalData: {}, // 弹框内数据
        modalIsMark: false, // 是否展示蒙层
        modalWidth: "850px", // 弹出层宽度'
        modalMinWidth: "600px", // 最小宽度
        modalShow: false, // modal显示标识
        modalZIndex: "5", // 弹框层级
      },
      modalCableDetails: {
        modalData: [], // 弹框内数据
        modalIsMark: true, // 是否展示蒙层
        modalWidth: "50%", // 弹出层宽度'
        modalMinWidth: "1000px", // 最小宽度
        modalShow: false, // modal显示标识
        modalZIndex: "5", // 弹框层级
      },
      modalLightLetStandDetails: {
        modalData: {}, // 弹框内数据
        modalIsMark: true, // 是否展示蒙层
        modalWidth: "850px", // 弹出层宽度'
        modalMinWidth: "300px", // 最小宽度
        modalShow: false, // modal显示标识
        modalZIndex: "5", // 弹框层级
      },
      modalLightLetStandBoardCardBeforeDetails: {
        modalData: {}, // 弹框内数据
        modalIsMark: false, // 是否展示蒙层
        modalWidth: "1540px", // 弹出层宽度'
        modalMinWidth: "1540px", // 最小宽度
        modalShow: false, // modal显示标识
        modalZIndex: "15", // 弹框层级
      },
      modalLightLetStandBoardCardDetails: [
        {
          key: "",
          title: "",
          modalData: {}, // 弹框内数据
          modalIsMark: false, // 是否展示蒙层
          modalWidth: "1540px", // 弹出层宽度'
          modalMinWidth: "1540px", // 最小宽度
          modalShow: false, // modal显示标识
          modalZIndex: "15", // 弹框层级
        },
        {
          key: "",
          title: "",
          modalData: {}, // 弹框内数据
          modalIsMark: false, // 是否展示蒙层
          modalWidth: "1540px", // 弹出层宽度'
          modalMinWidth: "1540px", // 最小宽度
          modalShow: false, // modal显示标识
          modalZIndex: "15", // 弹框层级
        },
      ],
      menuArr: ref({
        menuArrSearchVal: "",
        menuArrActive: "",
        menuArrOpens: [],
        menuArrSearchData: [],
        menuArrData: [],
        menuArrTransitData: [],
      }),
    };
  },
  components: {
    Modal,
    Exmodal,
  },
  watch: {},
  created() {
    this.computedMenuArray();
  },
  mounted() {
    this.init();
    this.initSize();
  },
  beforeRouteLeave(to, form, next) {
    window.onresize = null;
    next();
  },
  methods: {
    createGraph() {
      let _this = this;
      const container = document.getElementById("container");
      //container.appendChild(descriptionDiv);
      const width = container.scrollWidth;
      const height = container.scrollHeight;
      const minimap = new G6.Minimap({
        size: [180, 180],
        className: "minimap",
        type: "delegate",
      });
      // 创建 G6 图实例
      let res = new G6.Graph({
        container: "container", // 指定图画布的容器 id，与第 9 行的容器对应
        // 画布宽高
        width: width,
        height: height,
        linkCenter: true,
        fitView: true,
        fitCenter: true,
        animate: true,
        modes: {
          default: ["drag-canvas", "zoom-canvas", "drag-node"],
        },
        layout: {
          // type: "mds",
          linkDistance: 180,
          preventOverlap: true, // 防止节点重叠
        },
        linkCenter: true,
        maxStep: 1,
        maxZoom: 10,
        minZoom: 0.05,
        plugins: [minimap],
      });
      res.on("edge:dblclick", (e) => {
        _this.onEdgeDblClick(e);
      });
      res.on("node:dblclick", (e) => {
        _this.onNodeClick(e.item);
      });
      res.on("node:dragend", (e) => {
        _this.onNodeDragEnd(e);
      });
      res.on("edge:mouseenter", (e) => {
        res.setItemState(e.item, "hover", true);
      });
      res.on("edge:mouseleave", (e) => {
        res.setItemState(e.item, "hover", false);
      });
      return res;
    },
    getCurrentGraph() {
      if (this.graphLocal == null) {
        this.graphLocal = this.createGraph();
      }
      return this.graphLocal;
    },
    drawGraph(src) {
      let _this = this;
      let graph = this.getCurrentGraph();
      graph.clear();
      graph.get("canvas").set("localRefresh", false); // 关闭局部刷新，避免拖拽产生阴影
      graph.data(src);
      if (src.nodes[0].x == 0 && src.nodes[src.nodes.length - 1].x == 0) {
        // graph.cfg.layout.type = "mds";
        graph.updateLayout({
          type: "mds",
        });
      } else {
        graph.updateLayout({
          type: "",
        });
      }
      graph.render();
      graph.refresh();
      // graph.layout();
      // graph.fitCenter();
      graph.fitView();
      _this.canvasLoading = false;
    },
    zoomGraph(ratio) {
      let graph = this.getCurrentGraph();
      graph.zoomTo(ratio);
    },
    SetImgAndDraw(data) {
      let _this = this;
      const datas = data;
      if (!datas.edges && !datas.nodes && !datas.system_details) {
        _this.systemAbnormal = true;
        _this.canvasLoading = false;
        return;
      }
      var nodes_tmp;
      var edges_tmp;
      const system_Details = datas.system_details;
      if (system_Details) {
        _this.system_DetailsIsShow = true;
        _this.systemAbnormal = false;
        _this.system_Details = system_Details;
      } else {
        _this.system_DetailsIsShow = false;
        _this.systemAbnormal = true;
      }
      nodes_tmp = datas.nodes;
      nodes_tmp.forEach(function (item) {
        function ampCheck(isHigh) {
          switch (isHigh) {
            case 2:
              return icon_amp_red;
            case 1:
              return icon_amp_yellow;
            default:
              return icon_amp;
          }
        }
        function nodeCheck(isHigh) {
          switch (isHigh) {
            case 2:
              return icon_node_red;
            case 1:
              return icon_node_yellow;
            default:
              return icon_node;
          }
        }
        item.labelCfg = {
          position: "top",
          offset: 20,
          style: {
            fontSize: 40,
          },
        };
        switch (item.nodeType) {
          case 1:
            item.img = nodeCheck(item.isHigh);
            break;
          case 2:
            item.img = ampCheck(item.isHigh);
            break;
          default:
            item.img = nodeCheck(item.isHigh);
            return;
        }
      });
      // 假图片 Node
      edges_tmp = datas.edges;
      edges_tmp.forEach(function (item) {
        switch (item.isHigh) {
          case 2:
            item.style = {
              stroke: "#F93E3E",
              lineWidth: 10,
            };
            break;
          case 1:
            item.style = {
              stroke: "#F4E34E",
              lineWidth: 8,
            };
            break;
          default:
            item.style = {
              stroke: "#4e5ff5",
              lineWidth: 5,
            };
            break;
        }
        item.label = _this.computedKM(item.label);
        item.labelCfg = {
          position: "top",
          offset: 20,
          style: {
            fontSize: 30,
            fontWeight: 900,
            fill: "#F55151",
          },
        };
      });
      _this.drawGraph({
        nodes: nodes_tmp,
        edges: edges_tmp,
      });
    },
    SetModalAttribute(modal_list, key, data, mainAct_stand, alterAct_stand, is_show) {
      for (let modal of modal_list) {
        if (modal.key == key) {
          modal.modalData = data;
          modal.modalShow = is_show;
          modal.mainAct_stand = mainAct_stand;
          modal.alterAct_stand = alterAct_stand;
          return;
        }
      }
      // try find the first modalShow is false
      if (is_show) {
        if (!modal_list[0].modalShow) {
          modal_list[0].key = key;
          modal_list[0].modalData = data;
          modal_list[0].modalShow = is_show;
          modal_list[0].mainAct_stand = mainAct_stand;
          modal_list[0].alterAct_stand = alterAct_stand;
        } else if (!modal_list[1].modalShow) {
          modal_list[1].key = key;
          modal_list[1].modalData = data;
          modal_list[1].modalShow = is_show;
          modal_list[1].mainAct_stand = mainAct_stand;
          modal_list[1].alterAct_stand = alterAct_stand;
        } else {
          modal_list[0].key = key;
          modal_list[0].modalData = data;
          modal_list[0].modalShow = is_show;
          modal_list[0].mainAct_stand = mainAct_stand;
          modal_list[0].alterAct_stand = alterAct_stand;
        }
      }
    },
    SetMainMuxBoardDetail(modal_list, key, title, data, act_standArr, is_show) {
      for (let modal of modal_list) {
        if (modal.key == key) {
          modal.modalData = data;
          modal.modalShow = is_show;
          modal.act_standArr = act_standArr;
          modal.title = title;
          return;
        }
      }
      if (is_show) {
        if (!modal_list[0].modalShow) {
          modal_list[0].key = key;
          modal_list[0].modalData = data;
          modal_list[0].modalShow = is_show;
          modal_list[0].act_standArr = act_standArr;
          modal_list[0].title = title;
        } else if (!modal_list[1].modalShow) {
          modal_list[1].key = key;
          modal_list[1].modalData = data;
          modal_list[1].modalShow = is_show;
          modal_list[1].act_standArr = act_standArr;
          modal_list[1].title = title;
        } else {
          modal_list[0].key = key;
          modal_list[0].modalData = data;
          modal_list[0].modalShow = is_show;
          modal_list[0].act_standArr = act_standArr;
          modal_list[0].title = title;
        }
      }
    },
    SetOaDetail(modal_list, key, title, data, is_show, parent = null) {
      for (let modal of modal_list) {
        if (modal.key == key) {
          modal.modalData = data;
          modal.modalShow = is_show;
          modal.title = title;
          if (parent !== null && parent !== undefined) {
            if (parent.child?.modalShow && parent.child.key !== key && is_show) {
              parent.child.modalShow = false;
            }
            parent.child = modal;
          }
          return;
        }
      }
      if (is_show) {
        let tmp_modal = null;
        if (!modal_list[0].modalShow) {
          tmp_modal = modal_list[0];
        } else if (!modal_list[1].modalShow) {
          tmp_modal = modal_list[1];
        } else {
          tmp_modal = modal_list[0];
        }
        tmp_modal.key = key;
        tmp_modal.modalData = data;
        tmp_modal.modalShow = is_show;
        tmp_modal.title = title;
        if (parent !== null && parent !== undefined) {
          if (parent.child?.modalShow && parent.child.key !== key) {
            parent.child.modalShow = false;
          }
          parent.child = tmp_modal;
        }
      }
    },
    onNodeClick(item) {
      let _this = this;
      switch (item._cfg.model.nodeType) {
        case 1:
          let mainEdges = {
            sys_name: _this.defaultActive.sys_name,
            self: item._cfg.id,
          };
          getMain(mainEdges).then((res) => {
            if (res.code == 200) {
              const data = res.data;
              const length = data.mainFingerprint.length;
              const index = data.sub_nameArr.findIndex((find) =>
                find.act_stand.includes("备")
              );
              const type = data.type;

              if (type.includes("OADM") && length > 4 && length <= 8 && index < 0) {
                //ROADM没有主备-8-OA
                // _this.modalMainRoadmBoardDetail.modalData = res.data;
                // _this.modalMainRoadmBoardDetail.modalShow = true;
                // this.mainAct_stand = "";
                // this.alterAct_stand = "";
                this.SetModalAttribute(modalMainRoadmBoardDetails, mainEdges.self, res.data, "", "", true);
              } else if (
                type.includes("OADM") &&
                length > 4 &&
                length <= 8 &&
                index >= 0
              ) {
                //ROADM有主备-8-OA
                // _this.modalMainRoadmBoardDetail.modalData = res.data;
                // _this.modalMainRoadmBoardDetail.modalShow = true;
                // this.mainAct_stand = "主路由";
                // this.alterAct_stand = "备路由";
                this.SetModalAttribute(_this.modalMainRoadmBoardDetails, mainEdges.self, res.data, "主路由", "备路由", true);
              } else if (length > 4 && length <= 8 && index >= 0) {
                //OLP-8-OA
                _this.modalMainOlpBoardDetails.modalData = res.data;
                _this.modalMainOlpBoardDetails.modalShow = true;
              } else if (type.includes("OTM") && length > 4 && length <= 8 && index < 0) {
                //MUX2-8-OA
                _this.modalMainBoardDetails.modalData = res.data;
                _this.modalMainBoardDetails.modalShow = true;
              } else if (type.includes("OTM") && length > 2 && length <= 4 && index < 0) {
                //MUX-4-OA
                // _this.modalMainMuxBoardDetail.title = "MUX";
                // _this.modalMainMuxBoardDetail.modalData = res.data;
                // _this.modalMainMuxBoardDetail.modalShow = true;
                // _this.act_standArr = ["主路由", "主路由"];
                this.SetMainMuxBoardDetail(_this.modalMainMuxBoardDetails, mainEdges.self, "MUX", res.data, ["主路由", "主路由"], true);
              } else if (
                type.includes("OADM") &&
                length > 2 &&
                length <= 4 &&
                index < 0
              ) {
                //ROADM-4-OA
                // _this.modalMainMuxBoardDetail.title = "OADM";
                // _this.modalMainMuxBoardDetail.modalData = res.data;
                // _this.modalMainMuxBoardDetail.modalShow = true;
                // _this.act_standArr = ["主路由", "主路由"];
                this.SetMainMuxBoardDetail(_this.modalMainMuxBoardDetails, mainEdges.self, "OADM", res.data, ["主路由", "主路由"], true);
              } else if (type.includes("OTM") && length > 0 && length <= 2) {
                //MUX单向-2-OA
                _this.modalMainMuxSingleBoardDetails.title = "MUX";
                _this.modalMainMuxSingleBoardDetails.modalData = res.data;
                _this.modalMainMuxSingleBoardDetails.modalShow = true;
              } else if (type.includes("OADM") && length > 0 && length <= 2) {
                //ROADM单向-2-OA
                _this.modalMainMuxSingleBoardDetails.title = "OADM";
                _this.modalMainMuxSingleBoardDetails.modalData = res.data;
                _this.modalMainMuxSingleBoardDetails.modalShow = true;
              } else if (
                type.includes("OTM") &&
                length > 2 &&
                length <= 4 &&
                index >= 0
              ) {
                //MUX单层有主备
                // _this.modalMainMuxBoardDetail.title = "MUX";
                // _this.modalMainMuxBoardDetail.modalData = res.data;
                // _this.modalMainMuxBoardDetail.modalShow = true;
                // _this.act_standArr = ["主路由", "备路由"];
                this.SetMainMuxBoardDetail(_this.modalMainMuxBoardDetails, mainEdges.self, "MUX", res.data, ["主路由", "备路由"], true);
              } else if (
                type.includes("OADM") &&
                length > 2 &&
                length <= 4 &&
                index >= 0
              ) {
                //OADM单层有主备
                // _this.modalMainMuxBoardDetail.title = "OADM";
                // _this.modalMainMuxBoardDetail.modalData = res.data;
                // _this.modalMainMuxBoardDetail.modalShow = true;
                // _this.act_standArr = ["主路由", "备路由"];
                this.SetMainMuxBoardDetail(_this.modalMainMuxBoardDetails, mainEdges.self, "OADM", res.data, ["主路由", "备路由"], true);
              }
            } else {
              ElMessage({
                type: "error",
                message: "资源异常",
                offset: 200,
              });
            }
          });
          break;
        case 2:
          let alterEdges = {
            sys_name: _this.defaultActive.sys_name,
            self: item._cfg.id,
          };
          getOla(alterEdges).then((res) => {
            if (res.code == 200) {
              _this.modalLightLetStandDetails.modalData = res.data;
              _this.modalLightLetStandDetails.modalShow = true;
            } else {
              ElMessage({
                type: "error",
                message: "资源异常",
                offset: 200,
              });
            }
          });
          break;
      }
    },
    onNodeDragEnd(e) {
      let _this = this;
      const is_Authen = getIs_Authen();
      if (is_Authen.can_save_topo_position) {
        const username = getUserName();
        const data = {
          user_name: username,
          sys_name: _this.defaultActive.sys_name,
          ne_id: e.item._cfg.id,
          x: e.x,
          y: e.y,
          canvasx: e.canvasX,
          canvasy: e.canvasY,
          clientx: e.clientX,
          clienty: e.clientY,
        };
        setPosition(data);
      }
    },
    onEdgeDblClick(e) {
      // 双击光缆
      let _this = this;
      const data = e.item._cfg.model;
      const fiber_data = {
        source_ne_id: data.source,
        target_ne_id: data.target,
        act_stand: data.act_stand,
      };
      getFiber(fiber_data).then((res) => {
        if (res.code == 200) {
          _this.modalCableDetails.modalShow = true;
          _this.modalCableDetails.modalData = res.data;
        } else {
          ElMessage({
            type: "error",
            message: "资源异常",
            offset: 200,
          });
        }
      });
    },
    init() {
      let _this = this;
      _this.canvasLoading = true;
      _this.system_DetailsIsShow = false;
      if (_this.defaultActive.sys_name == "") {
        _this.canvasLoading = false;
        return;
      }
      getDraw(_this.defaultActive).then((res) => {
        if (res.code == 200) {
          _this.SetImgAndDraw(res.data);
        }
      });
    },
    initSize() {
      let _this = this;
      window.onresize = _.debounce(() => {
        const box = document.getElementById("container");
        _this.getCurrentGraph().changeSize(box.scrollWidth, box.scrollHeight);
        _this.getCurrentGraph().fitCenter();
        _this.getCurrentGraph().fitView();
      }, 300);
    },
    selectModalExit(modal_list, key) {
      for (let modal of modal_list) {
        if (modal.key == key) {
          modal.modalShow = false;
          if (modal.child !== null && modal.child !== undefined) {
            modal.child.modalShow = false;
          }
          break;
        }
      }
    },
    modalExit(id) {
      let _this = this;

      let idx = id.indexOf("::");
      let cmd = "";
      let self = "";
      if (idx >= 0) {
        cmd = id.substring(0, idx);
        self = id.substring(idx+2);
      } else {
        cmd = id;
      }

      switch (cmd) {
        case "MUX2":
          _this.modalMainBoardDetails.modalShow = false;
          break;
        case "MUX":
          // _this.modalMainMuxBoardDetail.modalShow = false;
          _this.selectModalExit(_this.modalMainMuxBoardDetails, self);
          break;
        case "ROADM":
          // _this.modalMainRoadmBoardDetail.modalShow = false;
          _this.selectModalExit(_this.modalMainRoadmBoardDetails, self);
          break;
        case "OLP":
          _this.modalMainOlpBoardDetails.modalShow = false;
          break;
        case "CABLE":
          _this.modalCableDetails.modalShow = false;
          break;
        case "OLA":
          _this.modalLightLetStandDetails.modalShow = false;
          break;
        case "OA":
          // _this.modalLightLetStandBoardCardBeforeDetails.modalShow = false;
          _this.selectModalExit(_this.modalLightLetStandBoardCardDetails, self);
          break;
        case "MUX/ROADM":
          _this.modalMainMuxSingleBoardDetails.modalShow = false;
      }
    },
    computedKM(data) {
      return Math.round(Math.trunc(data) / 1000) + "km";
    },
    handleScroll(e) {
      let direction = e.deltaY > 0 ? "down" : "up"; //deltaY为正则滚轮向下，为负滚轮向上
      let isUp = null;
      if (direction == "down" && e.deltaY >= 125) {
        //125为用户一次滚动鼠标的wheelDelta的值
        isUp = false;
      }
      if (direction == "up" && e.deltaY <= -125) {
        isUp = true;
      }
      if (isUp == null) {
        return;
      }
      let ratio = this.getCurrentRatio(isUp);
      this.zoomGraph(ratio);
    },
    getCurrentRatio(isUp) {
      let variable = isUp ? 0.1 : -0.1;
      ratioLocal += variable;
      if (ratioLocal < 0.1) {
        ratioLocal = 0.1; //   variable = isUp ? 0.01 : -0.01; //   ratioLocal += variable //   if(ratioLocal < 0.01){ //       ratioLocal = 0.01 //   }
      }
      if (ratioLocal > 10) {
        ratioLocal = 10;
      }
      return ratioLocal;
    },
    zoomInOn(IsZoom) {
      let variable = IsZoom ? 0.05 : -0.05;
      this.ratioLocal += variable;
      if (this.ratioLocal < 0.1) {
        this.ratioLocal = 0.1;
      }
      if (this.ratioLocal > 10) {
        this.ratioLocal = 10;
      }
      this.zoomGraph(this.ratioLocal);
    },
    selectOaContent(oa_fingerprint, parent = null) {
      let _this = this;
      let req_data = {
        oa_fingerpring: oa_fingerprint,
      };
      getOa(req_data).then((res) => {
        if (res.code == 200) {
          const data = res.data;
          // if (data.pre_position_Voa) {
          //  // 前置
          //   _this.modalLightLetStandBoardCardBeforeDetails.modalData = data;
          //   _this.modalLightLetStandBoardCardBeforeDetails.modalShow = true;
          // } else {
          //  // 后置
          //  _this.modalLightLetStandBoardCardDetails.modalData = data;
          //  _this.modalLightLetStandBoardCardDetails.modalShow = true;
          this.SetOaDetail(_this.modalLightLetStandBoardCardDetails, req_data.oa_fingerpring, "", data, true, parent);
          // }
        } else {
          ElMessage({
            type: "error",
            message: "资源异常",
            offset: 200,
          });
        }
      });
    },
    getSlotInfo(oa_fingerprint) {
      let idx = oa_fingerprint.indexOf("/");
      let slot_info = oa_fingerprint.substring(idx+1);
      return slot_info;
    },
    computedMenuArray() {
      let _this = this;
      _this.navigationLoading = true;
      let data = {
        username: getUserName(),
      };
      getMenu(data).then((res) => {
        if (res.code == 200) {
          _this.menuArr.menuArrTransitData = _this.menuArr.menuArrData = res.data;
          _this.navigationLoading = false;
        }
      });
    },
    selectItems(val) {
      let _this = this;
      if (_this.defaultActive.code != val) {
        _this.defaultActive = {
          perms: true,
          code: val,
          sys_name: val,
          user_name: getUserName(),
        };
        _this.init();
      }
    },
    Search() {
      let _this = this;
      Promise.resolve().then(() => {
        _this.navigationLoading = true;
        const serachVal = this.menuArr.menuArrSearchVal.replaceAll(" ", "");
        if (serachVal == "") {
          _this.menuArr.menuArrTransitData = _this.menuArr.menuArrData;
          _this.navigationLoading = false;
          return;
        }
        const menuArrSearchData = [];
        const menuArrOpens = [];

        for (let item of _this.menuArr.menuArrData) {
          if (item.name.includes(serachVal)) {
            menuArrSearchData.push(item);
            if (!menuArrOpens.includes(item.code)) {
              menuArrOpens[menuArrOpens.length] = item.code;
            }
            continue;
          } else {
            if (item.children.length > 0) {
              const chilData = JSON.parse(JSON.stringify(item));
              chilData.children = [];
              let isInclude = false;
              for (let chil of item.children) {
                if (chil.name.includes(serachVal)) {
                  isInclude = true;
                  chilData.children.push(chil);
                  if (!menuArrOpens.includes(item.code)) {
                    menuArrOpens[menuArrOpens.length] = item.code;
                  }
                }
              }
              if (isInclude) {
                menuArrSearchData.push(chilData);
              }
            }
          }
        }
        _this.menuArr.menuArrTransitData = menuArrSearchData;
        for (let i = 0; i < menuArrOpens.length; i++) {
          _this.menuArr.menuArrOpens[i] = menuArrOpens[i];
        }
        _this.navigationLoading = false;
      });
    },
    CheckState(val) {
      switch (val) {
        case 1:
          return "2px solid #FFA600";
        case 2:
          return "2px solid #F70004";
        default:
          return "2px solid #8394f8";
      }
    },
  },
};
</script>
<style scoped lang="scss">
@import "@/plugins/styles/WDM-OTN/transmissionSystem/index.scss";
</style>

<style>
div.minimap {
  position: absolute;
  padding: 0px;
  bottom: 10px;
  right: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  /* border: 1px solid #edeffe;
  border: 1px solid rgba(78, 95, 245, 0.5); */
  border-radius: 10px;
  box-sizing: border-box;
  border: 1px solid #eceff4;
}

.singleton-tooltip {
  transition: transform 0.3s var(--el-transition-function-fast-bezier);
}
.slot-info-one {
  padding: 50px;
  position: absolute;
  left: 43%;
  transform:translateX(-50%);
  color: var(--theme-color);
  font-size: 16px;
  bottom: -10%;
}
.ola-slot-info-one {
  padding: 50px;
  position: absolute;
  left: 50%;
  transform:translateX(-50%);
  color: var(--theme-color);
  font-size: 16px;
  bottom: 39%;
}
.slot-info-two {
  padding: 50px;
  position: absolute;
  left: 50%;
  transform:translateX(-50%);
  color: var(--theme-color);
  font-size: 16px;
}
.ola-slot-info-two {
  padding: 50px;
  position: absolute;
  left: 50%;
  transform:translateX(-50%);
  color: var(--theme-color);
  font-size: 16px;
  bottom: -7%;
}
.ola-slot-info-three {
  padding: 50px;
  position: absolute;
  left: 50%;
  transform:translateX(-50%);
  color: var(--theme-color);
  font-size: 16px;
  bottom: -122%;
}
</style>
