<template>
    <div
      :class="[modalIsMark == true ? 'modalMark modalIsMark': '', 'draggable']"
      v-if="modalShow"
      :style="{ 'z-index': modalZIndex }"
      @mousedown="startDrag"
    >
      <div
        class="modal"
        id="Modal"
        ref="modalRef"
        :style="{ 
          width: modalWidth,
          'min-width': modalMinWidth,
          transform: `translate(${dragX}px, ${dragY}px) scale(${scale})` }"
        :class="[modalShow == true ? 'modalShow' : 'modalExit', isMouseDown ? 'modalActive' : '']"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
      >
        <div class="modalContent">
          <svg
            @click="confirmModal(false)"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-x modalExit"
            viewBox="0 0 16 16"
          >
            <path
              d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
            />
          </svg>
          <div class="modalTitle" :class="{ Disabled: true }">
            <label class="title" for="Modal">{{ modalTitle }}</label>
          </div>
          <div class="modalBody">
            <slot />
          </div>
          <div class="modalFooter" :class="{ Disabled: true }">
            <button class="cancel" @click="confirmModal(false)">Cancel</button>
            <button class="confirm" @click="confirmModal(true)">Confirm</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  // 引入路由
  import { reactive, toRefs, ref, onMounted, onUnmounted } from "vue";
  
  export default {
    name: "exmodal",
    props: {
      modalShow: {
        type: Boolean,
        default: false,
      },
      modalTitle: {
        type: String,
        default: "",
      },
      modalIsMark: {
        type: Boolean,
        default: true,
      },
      modalWidth: {
        type: String,
        default: null,
      },
      modalMinWidth: {
        type: String,
        default: "300px",
      },
      modalIsConfirm: {
        type: Boolean,
        default: true,
      },
      modalZIndex: {
        type: String,
        default: "5",
      },
      key: {
        type: String,
        default: "",
      },
    },
    setup(props, content) {
      const modalRef = ref(null);

      const confirmModal = (sign) => {
        content.emit("confirmModal", sign);
      };
  
      const data = reactive({
        modalShow: props.modalShow,
        isMouseDown: false,
      });
      const dataRef = toRefs(data);
  
      const dragData = reactive({
        isDragging: false,
        startX: 0,
        startY: 0,
        dragX: 0,
        dragY: 0,
        scale: 1,
        in_modal: false,
      });

      onMounted(() => {
        const handleWheel = (e) => {
          e.preventDefault();
          dragData.scale += e.deltaY * -0.001;
        };
        // Bind the wheel event to the modalContentRef value
        modalRef.value.addEventListener('wheel', handleWheel);
      });

      const handleMouseEnter = () => {
        console.info('enter modal');
        dragData.in_modal = true;
      };

      const handleMouseLeave = () => {
        console.info('leave modal');
        dragData.in_modal = false;
      };
  
      const startDrag = (e) => {
        console.info("key down, startDrag");
        dragData.isDragging = true;
        dragData.startX = e.clientX - dragData.dragX;
        dragData.startY = e.clientY - dragData.dragY;

        // 设置isMouseDown为true
        if (!data.isMouseDown){
          data.isMouseDown = true;
          props.modalZIndex = (1 + props.modalZIndex).toString();
        }
        document.addEventListener("mousemove", handleDrag);
        document.addEventListener("mouseup", stopDrag);
      };
  
      const startDragBound = startDrag.bind(this);
  
      const stopDrag = () => {
        dragData.isDragging = false;
  
        document.removeEventListener("mousemove", handleDrag);
        document.removeEventListener("mouseup", stopDrag);
      };
  
      const handleDrag = (e) => {
  
        if (!dragData.isDragging) return;
  
        const offsetX = e.clientX - dragData.startX;
        const offsetY = e.clientY - dragData.startY;
  
        dragData.dragX = offsetX;
        dragData.dragY = offsetY;
      };
  
      document.addEventListener("keydown", function (e) {
        if (e.keyCode == 27) {
          confirmModal(false);
          return;
        }
      });

      document.addEventListener("mousedown", function (e) {
        // 如果鼠标点击的区域不是modal内部，则设置isMouseDown为false
        // if (!e.target.closest(".modal") && !dragData.in_modal) {
        //   data.isMouseDown = false;
        // }
        if (!dragData.in_modal) {
          if (data.isMouseDown) {
            data.isMouseDown = false;
            props.modalZIndex = (props.modalZIndex - 1).toString();
          }
        }
      });
  
      return {
        confirmModal,
        modalRef,
        ...dataRef,
        ...toRefs(dragData),
        startDrag: startDragBound,
        handleMouseEnter,
        handleMouseLeave,
      };
    },
  };
  </script>
  
  <style scoped lang="scss">
  
  .draggable {
    width: 100%;
    height: 20px;
    position: absolute;
    top: 350px; /* 调整此值以适应你的设计 */
    left: 0;
    cursor: grab;
  }
  
  .modalMark {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    font-family: "Microsoft YaHei";
    background-color: rgba(0, 0, 0, 0);
    animation: MarkHide 1s 1 forwards;
    overflow-x: hidden;
    overflow-y: hidden;
  }
  
  .modalMark.modalIsMark {
    animation: MarkShow 0.75s 1 forwards;
  }

  .modalContent {
    transform-origin: top left;
    transition: transform 0.2s;
  }
  
  .modal {
    position: absolute;
    // top: 50%;
    // left: 50%;
    top: -100%;
    left: 20%;
    // transform: translate(-50%, -150%) scale(0);
    // transform: translate(-50%, -50%) scale(0.85);
    transform: translate(-50%, -55%);
    // max-height: 90vh;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
    opacity: 0;
    z-index: 99 !important;
    width: inherit;
    width: initial;
    overflow: hidden;
    div.modalTitle {
      position: relative;
      width: 100%;
      padding: 8px calc(30px + 8px) 8px 8px;
      min-height: 50px;
      font-weight: 600;
      box-sizing: border-box;
      user-select: none;
      display: flex;
      align-items: center;
      align-content: flex-start;
      justify-content: flex-start;
      label.title {
        width: 100%;
        padding: 0 8px;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
      }
      svg.modalExit:hover {
        transition: color 0.15s ease-in;
        color: #333;
      }
    }
    div.modalTitle.Disabled {
      display: none;
    }
    svg.modalExit {
      position: absolute;
      right: 8px;
      top: 8px;
      /* transform: translateY(-50%); */
      width: 30px;
      height: 30px;
      color: #808080;
      border-radius: 6px;
      border: none;
      outline: none;
      user-select: none;
      cursor: pointer;
      z-index: 1;
    }
    div.modalBody {
      padding: 0 8px calc(50px + 8px) 8px;
      padding: 8px;
      width: 100%;
      min-height: 100px;
      /* max-height: 80vh; */
      box-sizing: border-box;
      /* overflow-anchor: none;
    overflow-x: hidden;
    overflow-y: auto;
    scrollbar-width: none;
    -ms-overflow-style: none; */
    }
    div.modalFooter {
      position: absolute;
      left: 0;
      bottom: 0;
      padding-right: 8px;
      width: 100%;
      height: 50px;
      min-height: 50px;
      box-sizing: border-box;
      background-color: #fff;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 8px;
      button.cancel {
        padding: 6px 14px 5px 14px;
        border: none;
        background-color: transparent;
        color: #333;
        letter-spacing: 0.5px;
        font-size: 16px;
        border-radius: 6px;
        cursor: pointer;
        text-align: center;
        line-height: auto;
        user-select: none;
      }
      button.confirm {
        padding: 6px 14px 5px 14px;
        background-color: #0d6efd;
        color: #fff;
        letter-spacing: 0.5px;
        font-size: 16px;
        border: none;
        border-radius: 6px;
        text-align: center;
        line-height: auto;
        cursor: pointer;
        user-select: none;
      }
      button.cancel,
      button.confirm {
        &:hover {
          background-color: #0b5ed7;
        }
      }
    }
    div.modalFooter.Disabled {
      display: none;
    }
    @keyframes showModal {
      100% {
        opacity: 1;
        // transform: translate(-50%, -50%) scale(1);
        // transform: translate(-50%, -50%);
      }
    }
    @keyframes hideModal {
      100% {
        opacity: 0;
        transform: translate(-50%, -55%);
      }
    }
  }
  // .modal:hover {
  //   background:lightsteelblue;
  // }
  .modal.modalShow {
    animation: showModal 0.3s 1 forwards;
  }

  .modal.modalActive {
    border-width: 2px;
    background:lightcyan;
  }
  
  .modal.modalExit {
    animation: hideModal 0.1s 1 forwards;
  }
  
  /* div#Modal.modal div.modalBody::-webkit-scrollbar {
    width: 0;
    height: 0;
  } */
  @keyframes MarkShow {
    100% {
      background-color: rgba(44, 44, 50, 0.6);
    }
  }
  
  @keyframes MarkHide {
    100% {
      background-color: rgba(44, 44, 50, 0);
    }
  }
  </style>
  